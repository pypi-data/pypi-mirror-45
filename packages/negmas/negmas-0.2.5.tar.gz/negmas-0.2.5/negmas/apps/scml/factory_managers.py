import itertools
from abc import abstractmethod, ABC
from collections import defaultdict

from negmas import Contract, Breach, Negotiator, MechanismState, AgentMechanismInterface, RenegotiationRequest, \
    JavaSAONegotiator, UtilityFunction, JavaUtilityFunction, _ShadowAgentMechanismInterface
from negmas.apps.scml.simulators import FactorySimulator, FastFactorySimulator
from negmas.apps.scml.simulators import storage_as_array, temporary_transaction
from negmas.common import NamedObject
from negmas.events import Notification
from negmas.helpers import get_class
from negmas.helpers import snake_case
from negmas.java import JavaCallerMixin, to_java, from_java, to_dict, java_link, PYTHON_CLASS_IDENTIFIER
from negmas.outcomes import Issue, Outcome
from negmas.utilities import UtilityValue
from .agent import SCMLAgent
from .awi import _ShadowSCMLAWI, SCMLAWI
from .common import SCMLAgreement, Factory, INVALID_UTILITY, CFP, Loan, ProductionFailure, FinancialReport
from .consumers import ScheduleDrivenConsumer, ConsumptionProfile
from .schedulers import Scheduler, ScheduleInfo, GreedyScheduler

if True:
    from typing import Dict, Iterable, Any, Callable, Collection, Type, List, Optional, Union

__all__ = [
    'FactoryManager', 'DoNothingFactoryManager', 'GreedyFactoryManager',
    'JavaFactoryManager', 'JavaDoNothingFactoryManager', 'JavaGreedyFactoryManager', 'JavaDummyMiddleMan',
]


class FactoryManager(SCMLAgent, ABC):
    """Base factory manager class that will be inherited by participant negmas in ANAC 2019"""

    @property
    def type_name(self):
        return super().type_name.replace('_factory_manager', '')

    def __init__(self, name=None, simulator_type: Union[str, Type[FactorySimulator]] = FastFactorySimulator):
        super().__init__(name=name)
        self.transportation_delay = 0
        self.simulator: Optional[FactorySimulator] = None
        self.simulator_type: Type[FactorySimulator] = get_class(simulator_type, scope=globals())
        self.current_step = 0
        self.max_storage: int = 0

    def init_(self):
        state: Factory = self.awi.state
        self.current_step = state.next_step
        self.max_storage = state.max_storage
        self.simulator = self.simulator_type(initial_wallet=state.wallet, initial_storage=state.storage
                                             , n_steps=self.awi.n_steps, n_products=len(self.awi.products)
                                             , profiles=state.profiles, max_storage=self.max_storage)
        super().init_()

    def step_(self):
        state = self.awi.state
        self.simulator.set_state(self.current_step, wallet=state.wallet, loans=state.loans
                                 , storage=storage_as_array(state.storage, n_products=len(self.products))
                                 , line_schedules=state.line_schedules)
        self.current_step += 1
        self.step()

    @abstractmethod
    def on_production_failure(self, failures: List[ProductionFailure]) -> None:
        """
        Called with a list of `ProductionFailure` records on production failure

        Args:
            failures:

        Returns:

        """

    class Java:
        implements = ['jnegmas.apps.scml.factory_managers.FactoryManager']


class DoNothingFactoryManager(FactoryManager):
    """The default factory manager that will be implemented by the committee of ANAC-SCML 2019"""

    def on_new_report(self, report: FinancialReport):
        pass

    def init(self):
        pass

    def step(self):
        pass

    def on_neg_request_rejected(self, req_id: str, by: Optional[List[str]]):
        pass

    def on_neg_request_accepted(self, req_id: str, mechanism: AgentMechanismInterface):
        pass

    def on_negotiation_failure(self, partners: List[str], annotation: Dict[str, Any],
                               mechanism: AgentMechanismInterface, state: MechanismState) -> None:
        pass

    def on_negotiation_success(self, contract: Contract, mechanism: AgentMechanismInterface) -> None:
        pass

    def on_contract_signed(self, contract: Contract) -> None:
        pass

    def on_contract_cancelled(self, contract: Contract, rejectors: List[str]) -> None:
        pass

    def sign_contract(self, contract: Contract) -> Optional[str]:
        return self.id

    def on_contract_nullified(self, contract: Contract, bankrupt_partner: str, compensation: float) -> None:
        pass

    def on_agent_bankrupt(self, agent_id: str) -> None:
        pass

    def confirm_partial_execution(self, contract: Contract, breaches: List[Breach]) -> bool:
        return True

    def on_remove_cfp(self, cfp: 'CFP') -> None:
        pass

    def on_production_failure(self, failures: List[ProductionFailure]) -> None:
        pass

    def respond_to_negotiation_request(self, cfp: "CFP", partner: str) -> Optional[Negotiator]:
        return None

    def confirm_contract_execution(self, contract: Contract) -> bool:
        return True

    def set_renegotiation_agenda(self, contract: Contract, breaches: List[Breach]) -> Optional[RenegotiationRequest]:
        return None

    def respond_to_renegotiation_request(self, contract: Contract, breaches: List[Breach]
                                         , agenda: RenegotiationRequest) -> Optional[Negotiator]:
        return None

    def confirm_loan(self, loan: Loan, bankrupt_if_rejected: bool) -> bool:
        """called by the world manager to confirm a loan if needed by the buyer of a contract that is about to be
        breached"""
        return bankrupt_if_rejected

    def on_new_cfp(self, cfp: 'CFP') -> None:
        pass


class GreedyFactoryManager(DoNothingFactoryManager):
    """The default factory manager that will be implemented by the committee of ANAC-SCML 2019"""

    def on_production_failure(self, failures: List[ProductionFailure]) -> None:
        pass

    def confirm_loan(self, loan: Loan, bankrupt_if_rejected: bool) -> bool:
        return bankrupt_if_rejected

    def confirm_contract_execution(self, contract: Contract) -> bool:
        return True

    def set_renegotiation_agenda(self, contract: Contract, breaches: List[Breach]) -> Optional[RenegotiationRequest]:
        return None

    def respond_to_renegotiation_request(self, contract: Contract, breaches: List[Breach],
                                         agenda: RenegotiationRequest) -> Optional[Negotiator]:
        return None

    def __init__(self, name=None, simulator_type: Union[str, Type[FactorySimulator]] = FastFactorySimulator
                 , scheduler_type: Union[str, Type[Scheduler]] = GreedyScheduler
                 , scheduler_params: Optional[Dict[str, Any]] = None
                 , optimism: float = 0.0
                 , negotiator_type: Union[str, Type[Negotiator]] = 'negmas.sao.AspirationNegotiator'
                 , negotiator_params: Optional[Dict[str, Any]] = None
                 , n_retrials=5, use_consumer=True, reactive=True, sign_only_guaranteed_contracts=False
                 , riskiness=0.0, max_insurance_premium: float = -1.0):
        super().__init__(name=name, simulator_type=simulator_type)
        self.negotiator_type = get_class(negotiator_type, scope=globals())
        self.negotiator_params = negotiator_params if negotiator_params is not None else {}
        self.optimism = optimism
        self.ufun_factory: Union[Type[NegotiatorUtility], Callable[[Any, Any], NegotiatorUtility]]
        if optimism < 1e-6:
            self.ufun_factory = PessimisticNegotiatorUtility
        elif optimism > 1 - 1e-6:
            self.ufun_factory = OptimisticNegotiatorUtility
        else:
            self.ufun_factory: NegotiatorUtility = lambda agent, annotation: \
                AveragingNegotiatorUtility(agent=agent, annotation=annotation, optimism=self.optimism)
        self.max_insurance_premium = max_insurance_premium
        self.n_retrials = n_retrials
        self.n_neg_trials: Dict[str, int] = defaultdict(int)
        self.consumer = None
        self.use_consumer = use_consumer
        self.reactive = reactive
        self.sign_only_guaranteed_contracts = sign_only_guaranteed_contracts
        self.contract_schedules: Dict[str, ScheduleInfo] = {}
        self.riskiness = riskiness
        self.negotiation_margin = int(round(n_retrials * max(0.0, 1.0 - riskiness)))
        self.scheduler_type: Type[Scheduler] = get_class(scheduler_type, scope=globals())
        self.scheduler: Scheduler = None
        self.scheduler_params: Dict[str, Any] = scheduler_params if scheduler_params is not None else {}

    def total_utility(self, contracts: Collection[Contract] = ()) -> float:
        """Calculates the total utility for the agent of a collection of contracts"""
        if self.scheduler is None:
            raise ValueError('Cannot calculate total utility without a scheduler')
        min_concluded_at = self.awi.current_step
        min_sign_at = min_concluded_at + self.awi.default_signing_delay
        with temporary_transaction(self.scheduler):
            schedule = self.scheduler.schedule(contracts=contracts, assume_no_further_negotiations=False
                                               , ensure_storage_for=self.transportation_delay
                                               , start_at=min_sign_at)
        if not schedule.valid:
            return INVALID_UTILITY
        return schedule.final_balance

    def init(self):
        self.negotiation_margin = max(self.negotiation_margin,
                                      int(round(len(self.products) * max(0.0, 1.0 - self.riskiness))))
        if self.use_consumer:
            # @todo add the parameters of the consumption profile as parameters of the greedy factory manager
            profiles = dict(zip(self.consuming.keys(),
                                (ConsumptionProfile(schedule=[_] * self.awi.n_steps) for _ in itertools.repeat(0))))
            self.consumer: ScheduleDrivenConsumer = ScheduleDrivenConsumer(profiles=profiles
                                                                           , consumption_horizon=self.awi.n_steps,
                                                                           immediate_cfp_update=True
                                                                           , name=self.name)
            self.consumer.id = self.id
            self.consumer.awi = self.awi
            self.consumer.init_()
        self.scheduler = self.scheduler_type(manager_id=self.id, awi=self.awi
                                             , max_insurance_premium=self.max_insurance_premium
                                             , **self.scheduler_params)
        self.scheduler.init(simulator=self.simulator, products=self.products, processes=self.processes
                            , producing=self.producing, profiles=self.compiled_profiles)

    def respond_to_negotiation_request(self, cfp: "CFP", partner: str) -> Optional[Negotiator]:
        if self.awi.is_bankrupt(partner):
            return None
        if self.use_consumer:
            return self.consumer.respond_to_negotiation_request(cfp=cfp, partner=partner)
        else:
            neg = self.negotiator_type(name=self.name + '*' + partner, **self.negotiator_params)
            neg.utility_function = self.ufun_factory(self, self._create_annotation(cfp=cfp))
            neg.utility_function.reserved_value = cfp.money_resolution if cfp.money_resolution is not None else 0.1
            # neg.utility_function = normalize(self.ufun_factory(self, self._create_annotation(cfp=cfp)),
            #                                 outcomes=cfp.outcomes, infeasible_cutoff=0)
            return neg

    def on_negotiation_success(self, contract: Contract, mechanism: AgentMechanismInterface):
        if self.use_consumer:
            self.consumer.on_negotiation_success(contract, mechanism)

    def on_negotiation_failure(self, partners: List[str], annotation: Dict[str, Any], mechanism: AgentMechanismInterface
                               , state: MechanismState) -> None:
        if self.use_consumer:
            self.consumer.on_negotiation_failure(partners, annotation, mechanism, state)
        cfp = annotation['cfp']
        thiscfp = self.awi.bb_query(section='cfps', query=cfp.id, query_keys=True)
        if cfp.publisher != self.id and thiscfp is not None and len(thiscfp) > 0 \
            and self.n_neg_trials[cfp.id] < self.n_retrials:
            self.awi.logdebug(f'Renegotiating {self.n_neg_trials[cfp.id]} on {cfp}')
            self.on_new_cfp(cfp=annotation['cfp'])

    def _execute_schedule(self, schedule: ScheduleInfo, contract: Contract) -> None:
        if self.simulator is None:
            raise ValueError('No factory simulator is defined')
        awi: SCMLAWI = self.awi
        total = contract.agreement['unit_price'] * contract.agreement['quantity']
        product = contract.annotation['cfp'].product
        if contract.annotation['buyer'] == self.id:
            self.simulator.buy(product=product, quantity=contract.agreement['quantity']
                               , price=total, t=contract.agreement['time']
                               )
            if total <= 0 or self.max_insurance_premium < 0.0 or contract is None:
                return
            premium = awi.evaluate_insurance(contract=contract)
            if premium is None:
                return
            relative_premium = premium / total
            if relative_premium <= self.max_insurance_premium:
                awi.buy_insurance(contract=contract)
                self.simulator.pay(premium, self.awi.current_step)
            return
        # I am a seller
        self.simulator.sell(product=product, quantity=contract.agreement['quantity']
                            , price=total, t=contract.agreement['time'])
        for job in schedule.jobs:
            if job.action == 'run':
                awi.schedule_job(job, contract=contract)
            elif job.action == 'stop':
                awi.stop_production(line=job.line, step=job.time, contract=contract, override=job.override)
            else:
                awi.schedule_job(job, contract=contract)
            self.simulator.schedule(job=job, override=False)
        for need in schedule.needs:
            if need.quantity_to_buy <= 0:
                continue
            product_id = need.product
            # self.simulator.reserve(product=product_id, quantity=need.quantity_to_buy, t=need.step)
            if self.use_consumer:
                self.consumer.profiles[product_id].schedule[need.step] += need.quantity_to_buy
                self.consumer.register_product_cfps(p=product_id, t=need.step
                                                    , profile=self.consumer.profiles[product_id])
                continue
            product = self.products[product_id]
            if product.catalog_price is None:
                price_range = (0.0, 100.0)
            else:
                price_range = (0.5, 1.5 * product.catalog_price)
            # @todo check this. This error is raised sometimes
            if need.step < awi.current_step:
                continue
                # raise ValueError(f'need {need} at {need.step} while running at step {awi.current_step}')
            time = need.step if self.max_storage is not None else (awi.current_step, need.step)
            cfp = CFP(is_buy=True, publisher=self.id, product=product_id
                      , time=time, unit_price=price_range
                      , quantity=(1, int(1.1 * need.quantity_to_buy)))
            awi.register_cfp(cfp)

    def sign_contract(self, contract: Contract):
        if any(self.awi.is_bankrupt(partner) for partner in contract.partners):
            return None
        signature = self.id
        with temporary_transaction(self.scheduler):
            schedule = self.scheduler.schedule(assume_no_further_negotiations=False, contracts=[contract]
                                               , ensure_storage_for=self.transportation_delay
                                               , start_at=self.awi.current_step + 1)

        if self.sign_only_guaranteed_contracts and (not schedule.valid or len(schedule.needs) > 1):
            self.awi.logdebug(f'{self.name} refused to sign contract {contract.id} because it cannot be scheduled')
            return None
        # if schedule.final_balance <= self.simulator.final_balance:
        #     self.awi.logdebug(f'{self.name} refused to sign contract {contract.id} because it is not expected '
        #                       f'to lead to profit')
        #     return None
        if schedule.valid:
            profit = schedule.final_balance - self.simulator.final_balance
            self.awi.logdebug(f'{self.name} singing contract {contract.id} expecting '
                              f'{-profit if profit < 0 else profit} {"loss" if profit < 0 else "profit"}')
        else:
            self.awi.logdebug(f'{self.name} singing contract {contract.id} expecting breach')
            return None

        self.contract_schedules[contract.id] = schedule
        return signature

    def on_contract_signed(self, contract: Contract):
        if contract.annotation['buyer'] == self.id and self.use_consumer:
            self.consumer.on_contract_signed(contract)
        schedule = self.contract_schedules[contract.id]
        if schedule is not None and schedule.valid:
            self._execute_schedule(schedule=schedule, contract=contract)
        if contract.annotation['buyer'] != self.id or not self.use_consumer:
            for negotiation in self._running_negotiations.values():
                self.notify(negotiation.negotiator, Notification(type='ufun_modified', data=None))

    def _process_buy_cfp(self, cfp: 'CFP') -> None:
        if self.awi.is_bankrupt(cfp.publisher):
            return None
        if self.simulator is None or not self.can_expect_agreement(cfp=cfp, margin=self.negotiation_margin):
            return
        if not self.can_produce(cfp=cfp):
            return
        neg = self.negotiator_type(name=self.name + '>' + cfp.publisher, **self.negotiator_params)
        ufun = self.ufun_factory(self, self._create_annotation(cfp=cfp))
        ufun.reserved_value = cfp.money_resolution if cfp.money_resolution is not None else 0.1
        self.request_negotiation(negotiator=neg, cfp=cfp
                                 , ufun=ufun)
        #normalize(, outcomes=cfp.outcomes, infeasible_cutoff=-1)

    def _process_sell_cfp(self, cfp: 'CFP'):
        if self.awi.is_bankrupt(cfp.publisher):
            return None
        if self.use_consumer:
            self.consumer.on_new_cfp(cfp=cfp)

    def on_new_cfp(self, cfp: 'CFP') -> None:
        if not self.reactive:
            return
        if cfp.satisfies(query={'is_buy': True, 'products': list(self.producing.keys())}):
            self._process_buy_cfp(cfp)
        if cfp.satisfies(query={'is_buy': False, 'products': list(self.consuming.keys())}):
            self._process_sell_cfp(cfp)

    def step(self):
        if self.use_consumer:
            self.consumer.step()
        if self.reactive:
            return
        # 0. remove all my CFPs
        # self.awi.bb_remove(section='cfps', query={'publisher': self})

        # respond to interesting CFPs
        # todo: should check time and sort products by interest etc
        cfps = self.awi.bb_query(section='cfps'
                                 , query={'products': self.producing.keys(), 'is_buy': True})
        if cfps is None:
            return
        for cfp in cfps.values():
            self._process_buy_cfp(cfp)

    def can_produce(self, cfp: CFP, assume_no_further_negotiations=False) -> bool:
        """Whether or not we can produce the required item in time"""
        if cfp.product not in self.producing.keys():
            return False
        agreement = SCMLAgreement(time=cfp.max_time, unit_price=cfp.max_unit_price, quantity=cfp.min_quantity)
        min_concluded_at = self.awi.current_step + 1 - int(self.immediate_negotiations)
        min_sign_at = min_concluded_at + self.awi.default_signing_delay
        if cfp.max_time < min_sign_at + 1:  # 1 is minimum time to produce the product
            return False
        with temporary_transaction(self.scheduler):
            schedule = self.scheduler.schedule(contracts=[Contract(partners=[self.id, cfp.publisher]
                                                                   , agreement=agreement
                                                                   , annotation=self._create_annotation(cfp=cfp)
                                                                   , issues=cfp.issues, signed_at=min_sign_at
                                                                   , concluded_at=min_concluded_at)]
                                               , ensure_storage_for=self.transportation_delay
                                               , assume_no_further_negotiations=assume_no_further_negotiations
                                               , start_at=min_sign_at)
        return schedule.valid and self.can_secure_needs(schedule=schedule, step=self.awi.current_step)

    def can_secure_needs(self, schedule: ScheduleInfo, step: int):
        """
        Finds if it is possible in principle to arrange these needs at the given time.

        Args:
            schedule:
            step:

        Returns:

        """
        needs = schedule.needs
        if len(needs) < 1:
            return True
        for need in needs:
            if need.quantity_to_buy > 0 and need.step < step + 1 - int(self.immediate_negotiations):  # @todo check this
                return False
        return True


TotalUtilityFun = Callable[[Collection[Contract]], float]


class NegotiatorUtility(UtilityFunction):
    """The utility function of a negotiator."""

    def __init__(self, agent: GreedyFactoryManager, annotation: Dict[str, Any], name: Optional[str] = None):
        if name is None:
            name = agent.name + '*' + '*'.join(_ for _ in annotation['partners'] if _ != agent.id)
        super().__init__(name=name)
        self.agent = agent
        self.annotation = annotation

    def _contracts(self, agreements: Iterable[SCMLAgreement]) -> Collection[Contract]:
        """Converts agreements/outcomes into contracts"""
        if self.ami is None:
            raise ValueError('No annotation is stored (No mechanism info)')
        annotation = self.ami.annotation
        return [Contract(partners=annotation['partners'], agreement=a, annotation=annotation, issues=self.ami.issues)
                for a in agreements]

    def _contract(self, agreement: SCMLAgreement) -> Contract:
        """Converts an agreement/outcome into a contract"""
        annotation = self.annotation
        return Contract(partners=annotation['partners'], agreement=agreement
                        , annotation=annotation, issues=annotation['cfp'].issues)

    def _free_sale(self, agreement: SCMLAgreement) -> bool:
        return self.annotation['seller'] == self.agent.id and agreement['unit_price'] < 1e-6

    def __call__(self, outcome: Outcome) -> Optional[UtilityValue]:
        if isinstance(outcome, dict):
            return self.call(agreement=SCMLAgreement(**outcome))
        if isinstance(outcome, SCMLAgreement):
            return self.call(agreement=outcome)
        raise ValueError(f'Outcome: {outcome} cannot be converted to an SCMLAgreement')

    @abstractmethod
    def call(self, agreement: SCMLAgreement) -> Optional[UtilityValue]:
        """Called to evaluate a agreement"""

    def xml(self, issues: List[Issue]) -> str:
        return 'NegotiatorUtility has not xml representation'


class PessimisticNegotiatorUtility(NegotiatorUtility):
    """The utility function of a negotiator that assumes other negotiations currently open will fail."""

    def call(self, agreement: SCMLAgreement) -> Optional[UtilityValue]:
        """An offer will be a tuple of one value which in turn will be a list of contracts"""
        if self._free_sale(agreement):
            return INVALID_UTILITY
        # contracts = self.agent.contracts
        # hypothetical = list(contracts)
        # hypothetical.append(self._contract(agreement))
        hypothetical = [self._contract(agreement)]
        base_util = self.agent.simulator.final_balance
        hypothetical = self.agent.total_utility(hypothetical)
        if hypothetical < 0:
            return INVALID_UTILITY
        return hypothetical - base_util


class OptimisticNegotiatorUtility(NegotiatorUtility):
    """The utility function of a negotiator that assumes other negotiations currently open will succeed."""

    def call(self, agreement: SCMLAgreement) -> Optional[UtilityValue]:
        if self._free_sale(agreement):
            return INVALID_UTILITY
        # contracts = self.agent.contracts
        # hypothetical = list(contracts)
        # hypothetical.append(self._contract(agreement))
        hypothetical = [self._contract(agreement)]
        for negotiation in self.agent.running_negotiations:  # type: ignore
            negotiator = negotiation.negotiator
            current_offer = negotiator.my_last_proposal
            if current_offer is not None:
                hypothetical.append(self._contract(current_offer))
        base_util = self.agent.simulator.final_balance
        hypothetical = self.agent.total_utility(list(hypothetical))
        if hypothetical < 0:
            return INVALID_UTILITY
        return hypothetical - base_util


class AveragingNegotiatorUtility(NegotiatorUtility):
    """A utility function that combines optimistic and pessimistic evaluators linearly using adjustable weight"""

    def __init__(self, agent: GreedyFactoryManager, annotation: Dict[str, Any], name: Optional[str] = None
                 , optimism: float = 0.5):
        NamedObject.__init__(self=self, name=name)
        self.optimism = optimism
        self.optimistic = OptimisticNegotiatorUtility(agent=agent, annotation=annotation)
        self.pessimistic = PessimisticNegotiatorUtility(agent=agent, annotation=annotation)

    def call(self, agreement: SCMLAgreement) -> Optional[UtilityValue]:
        if self._free_sale(agreement):
            return INVALID_UTILITY
        opt, pess = self.optimistic(agreement), self.pessimistic(agreement)
        if opt is None or pess is None:
            return None
        return self.optimism * opt + (1 - self.optimism) * pess


class JavaFactoryManager(FactoryManager, JavaCallerMixin):
    """Allows factory managers implemented in Java (using jnegmas) to participate in SCML worlds.

    Objects of this class is used to represent a java object to the python environment. This means that they *MUST* have
    the same interface as a python class (first class in the inheritance list). The `JavaCallerMixin` is used to enable
    it to connect to the java object it is representing.

    """

    @property
    def type_name(self):
        """Overrides type name to give the internal java type name"""
        return 'j' + snake_case(self._java_class_name.replace('jnegmas.apps.scml.factory_managers.', '').replace(
            'FactoryManager', ''))

    @property
    def awi(self):
        return self._awi

    @awi.setter
    def awi(self, value):
        self._awi = value
        if self.python_shadow is not self:
            self.python_shadow._awi = value
        self.java_awi = _ShadowSCMLAWI(value)
        self._java_object.setAWI(self.java_awi)

    def init(self):
        if self.python_shadow is not self:
            self.python_shadow.simulator = self.simulator
        self._java_object.setSimulator(self.simulator)
        self._java_object.init()

    def step(self):
        return self._java_object.init()

    def on_neg_request_rejected(self, req_id: str, by: Optional[List[str]]):
        return self._java_object.onNegRequestRejected(req_id, by)

    def on_neg_request_accepted(self, req_id: str, mechanism: AgentMechanismInterface):
        return self._java_object.onNegRequestAccepted(req_id, java_link(_ShadowAgentMechanismInterface(mechanism)))

    def on_new_cfp(self, cfp: 'CFP'):
        return from_java(self._java_object.onNewCFP(to_java(cfp)))

    def on_remove_cfp(self, cfp: 'CFP'):
        return self._java_object.onRemoveCFP(to_java(cfp))

    def on_contract_nullified(self, contract: Contract, bankrupt_partner: str, compensation: float) -> None:
        self._java_object.onContractNullified(to_java(contract), bankrupt_partner, compensation)

    def on_agent_bankrupt(self, agent_id: str) -> None:
        self._java_object.onAgentBankrupt(agent_id)

    def confirm_partial_execution(self, contract: Contract, breaches: List[Breach]) -> bool:
        return self._java_object.confirmParialExecution(to_java(contract), to_java(breaches))

    def on_production_failure(self, failures: List[ProductionFailure]) -> None:
        return self._java_object.onProductionFailure(to_java(failures))

    def confirm_loan(self, loan: Loan, bankrupt_if_rejected: bool) -> bool:
        return self._java_object.confirmLoan(to_java(loan), bankrupt_if_rejected)

    def confirm_contract_execution(self, contract: Contract) -> bool:
        return self._java_object.confirmContractExecution(to_java(contract))

    def respond_to_negotiation_request(self, cfp: "CFP", partner: str) -> Optional[Negotiator]:
        result = self._java_object.respondToNegotiationRequest(to_java(cfp), partner)
        if result is None:
            return result
        return JavaSAONegotiator(java_object=result, java_class_name=None)

    def on_negotiation_failure(self, partners: List[str], annotation: Dict[str, Any], mechanism: AgentMechanismInterface
                               , state: MechanismState) -> None:
        return self._java_object.onNegotiationFailure(to_java(partners), annotation
                                                      , java_link(_ShadowAgentMechanismInterface(mechanism))
                                                      , to_java(state))

    def on_negotiation_success(self, contract: Contract, mechanism: AgentMechanismInterface) -> None:
        return self._java_object.onNegotiationSuccess(to_java(contract)
                                                      , java_link(_ShadowAgentMechanismInterface(mechanism)))

    def on_contract_signed(self, contract: Contract) -> None:
        return self._java_object.onContractSigned(to_java(contract))

    def on_contract_cancelled(self, contract: Contract, rejectors: List[str]) -> None:
        return self._java_object.onContractCancelled(to_java(contract), to_java(rejectors))

    def on_new_report(self, report: FinancialReport):
        pass

    def sign_contract(self, contract: Contract) -> Optional[str]:
        return from_java(self._java_object.signContract(to_java(contract)))

    def set_renegotiation_agenda(self, contract: Contract, breaches: List[Breach]) -> Optional[RenegotiationRequest]:
        return from_java(self._java_object.setRenegotiationAgenda(to_java(contract), to_java(breaches)))

    def respond_to_renegotiation_request(self, contract: Contract, breaches: List[Breach],
                                         agenda: RenegotiationRequest) -> Optional[Negotiator]:
        return from_java(self._java_object.respondToRenegotiationRequest(to_java(contract), to_java(breaches)
                                                                         , to_java(agenda)))

    # handy constructors
    @classmethod
    def do_nothing_manager(cls):
        return JavaFactoryManager(java_class_name='jnegmas.apps.scml.factory_managers.DoNothingFactoryManager')

    @classmethod
    def greedy_manager(cls):
        return JavaFactoryManager(java_class_name='jnegmas.apps.scml.factory_managers.GreedyFactoryManager')

    def __init__(self, java_object=None
                 , java_class_name: str = None
                 , python_shadow: Optional[FactoryManager] = None
                 , auto_load_java: bool = False
                 , name=None, simulator_type: Union[str, Type[FactorySimulator]] = FastFactorySimulator):
        super().__init__(name=name, simulator_type=simulator_type)
        self.java_awi = None
        if python_shadow is None:
            python_shadow_object = self
        else:
            python_shadow_object = python_shadow
        self.python_shadow = python_shadow_object
        self.init_java_bridge(java_object=java_object, java_class_name=java_class_name, auto_load_java=auto_load_java
                              , python_shadow_object=python_shadow_object)
        if java_object is None:
            map = to_dict(self)
            map.pop(PYTHON_CLASS_IDENTIFIER, None)
            map['simulatorType'] = self.simulator_type.__class__.__name__
            self._java_object.fromMap(to_java(map))

    def getNegotiationRequests(self):
        return to_java(self.requested_negotiations)

    def getRunningNegotiations(self):
        return to_java(self.running_negotiations)

    def requestNegotiation(self, cfp: CFP, negotiator: Negotiator = None, ufun: UtilityFunction = None) -> bool:
        return self.request_negotiation(from_java(cfp), JavaSAONegotiator(negotiator, None)
                                        , JavaUtilityFunction(ufun, None))

    class Java:
        implements = ['jnegmas.apps.scml.factory_managers.FactoryManager']


class JavaDoNothingFactoryManager(JavaFactoryManager):
    def __init__(self, auto_load_java: bool = False
                 , name=None, simulator_type: Union[str, Type[FactorySimulator]] = FastFactorySimulator):
        super().__init__(name=name, simulator_type=simulator_type, auto_load_java=auto_load_java
                         , java_class_name='jnegmas.apps.scml.factory_managers.DoNothingFactoryManager')


class JavaGreedyFactoryManager(JavaFactoryManager):
    def __init__(self, auto_load_java: bool = False
                 , name=None, simulator_type: Union[str, Type[FactorySimulator]] = FastFactorySimulator):
        super().__init__(name=name, simulator_type=simulator_type, auto_load_java=auto_load_java
                         , java_class_name='jnegmas.apps.scml.factory_managers.GreedyFactoryManager'
                         , python_shadow=lambda: GreedyFactoryManager(name=name
                                                                      , simulator_type=self.simulator_type))


class JavaDummyMiddleMan(JavaFactoryManager):
    def __init__(self, auto_load_java: bool = False
                 , name=None, simulator_type: Union[str, Type[FactorySimulator]] = FastFactorySimulator):
        super().__init__(name=name, simulator_type=simulator_type, auto_load_java=auto_load_java
                         , java_class_name='jnegmas.apps.scml.factory_managers.DummyMiddleMan')

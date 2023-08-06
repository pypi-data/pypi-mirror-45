# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# **************************************  GatingMechanism ************************************************

"""

Overview
--------

A GatingMechanism is an `AdaptiveMechanism <AdaptiveMechanism>` that modulates the value of the InputState(s) and/or
OutputState(s) of one or more `Mechanisms <Mechanism>`.   Its `function <GatingMechanism.function>` takes the
GatingMechanism's `variable <GatingMechanism.variable>` and uses that generate a `gating_policy`:  a list of values,
one for each of its `GatingSignals <GatingSignal>`.  Each of those, in turn, generates a `gating_signal
<GatingSignal.gating_signal>` used by its `GatingProjections <GatingProjection>` to modulate the value of the
State(s) to which they project.   A GatingMechanism can regulate only the parameters of Mechanisms in the `System`
to which it belongs.  The InputStates and/or OutputStates gated by a GatingMechanism can be list using its `show
<GatingMehanism.show>` method.

COMMENT: TBI
The gating components of a System can be displayed using the System's
`show_graph` method with its **show_gating** argument assigned as :keyword:``True`.
COMMENT

The gating components of a System are executed after all `ProcessingMechanisms <ProcessingMechanism>`,
`LearningMechanism <LearningMechanism>`, and  `ControlMechanism <ControlMechanism>` in that System have been executed.

.. _GatingMechanism_Creation:

Creating A GatingMechanism
---------------------------

GatingMechanism can be created using the standard Python method of calling the constructor for the desired type.
A GatingMechanism is also created automatically if `gating is specified <GatingMechanism_Specifying_Gating>` for an
`InputState`, `OutputState` or `Mechanism <Mechanism>`, in which case a `GatingProjection` is automatically created
that projects from the GatingMechanism to the specified target

.. _GatingMechanism_Specifying_Gating:

*Specifying gating*
~~~~~~~~~~~~~~~~~~~

GatingMechanism are used to modulate the value of an `InputState` or `OutputState`. An InputState or OutputState can
be specified for gating by assigning it a `GatingProjection` or `GatingSignal` anywhere that the Projections to a State
or its ModulatorySignals `can be specified <State_Creation>`.  A `Mechanism <Mechanism>` can also be specified for
gating, in which case the `primary InputState <InputState_Primary>` of the specified Mechanism is used.  States
(and/or Mechanisms) can also be specified in the  **gating_signals** argument of the constructor for a
GatingMechanism. The **gating_signals** argument must be a list, each item of which must refer to one or more States
(or the Mechanism(s) to which they belong) to be gated by that GatingSignal.  The specification for each item in the
list can use any of the forms used to `specify a GatingSignal <GatingSignal_Specification>`.


.. _GatingMechanism_GatingSignals:

GatingSignals
^^^^^^^^^^^^^

A `GatingSignal` is created for each item listed in the **gating_signals** argument of the constructor, and all of the
GatingSignals for a GatingMechanism are listed in its `gating_signals <GatingMechanism.gating_signals>` attribute.
Each GatingSignal is assigned one or more `GatingProjections <GatingProjection>` to the InputState(s) and/or
OutputState(s) it gates. By default, the `function <GatingMechanism.function>` of GatingMechanism generates a
a `value <GatingMechanism.value>` -- its `gating_policy <GatingSignal.gating_policy>` -- with a single item, that is
used by all of the GatingMechanism's GatingSignals.  However,  if a custom `function <GatingMechanism.function>` is
specified that generates a `gating_policy <GatingSignal.gating_policy>` with more than one item, different
GatingSignals can be assigned to the different items (see `GatingMechanism_Function` below).

.. _GatingMechanism_Modulation:

Modulation
^^^^^^^^^^

Each GatingMechanism has a `modulation <GatingSignal.modulation>` attribute, that provides a default for the way
in which its GatingSignals modulate the value of the States they gate
(see `modulation <ModulatorySignal_Modulation>` for an explanation of how this attribute is specified and used to
modulate the value of a State).  Each GatingSignal uses this value, unless its value is
`individually specified <GatingSignal_Modulation>`.

.. _GatingMechanism_Structure:

Structure
---------

.. _GatingMechanism_Input:

*Input*
~~~~~~~

By default, a GatingMechanism has a single `InputState`, the `value <InputState.value>` of which is used
as the input to the GatingMechanism's `function <GatingMechanism.function>`.

.. _GatingMechanism_Function:

*Function*
~~~~~~~~~~

A GatingMechanism's `function <GatingMechanism.function>` uses the `value <InputState.value>` of its `primary
InputState  <InputState_Primary>` to generate an `gating_policy <GatingMechanism.gating_policy>`.  The default
`function <GatingMechanism.function>` for a GatingMechanism is a `Linear` identity function, that simply takes
the `value <InputState.value>` of its `primary InputState <InputState_Primary>` and assigns this as the single item
of its `gating_policy <GatingMechanism.gating_policy>`.  This can be replaced by a `Function` that generates
a `gating_policy <GatingMechanism.gating_policy>` with multiple values, which may be useful if the GatingMechanism
is assigned more than one `GatingSignal`.

.. _GatingMechanism_Output:

*Output*
~~~~~~~~

A GatingMechanism has a `GatingSignal` for each `InputState` and/or `OutputState` specified in its `gating_signals
<GatingMechanism.gating_signals>` attribute, to which it sends a `GatingProjection`.  If the GatingMechanism's
`function <GatingMechanism.function>` generates a `gating_policy <GatingMechanism.gating_policy>` with a single value
(the default), then this is used as the `value <GatingSignal.value>` of all of the GatingMechanism's `gating_signals
<GatingMechanism.gating_signals>`.  If the `gating_policy <GatingMechanism.gating_policy>` has multiple items, and this
is the same as the number of GatingSignals, then each GatingSignal is assigned the value of the corresponding item in
the `gating_policy <GatingMechanism.gating_policy>`.  If there is a different number of `gating_signals
<GatingMechanism.gating_signals>` than the number of items in the `gating_policy <GatingMechanism.gating_policy>`,
then the `index <GatingSignal.index>` attribute of each GatingSignal must be specified (e.g., in a `specification
dictionary <GatingSignal_Specification>` in the **gating_signal** argument of the GatingMechanism's constructor),
or an error is generated.  The GatingSignals of a GatingMechanism are listed in its `gating_signals
<GatingMechanism.gating_signals>` attribute.  Since GatingSignals are a type of `OutputState`, they are also listed
in the GatingMechanism's `output_states <Mechanism_Base.output_states>` attribute. The InputStates and/or OutputStates
modulated by a GatingMechanism's GatingSignals can be displayed using its :func:`show <GatingMechanism.show>` method.

.. _GatingMechanism_Execution:

Execution
---------

A GatingMechanism executes in the same way as a `ProcessingMechanism <ProcessingMechanism>`, based on its place in the
System's `graph <System.graph>`.  Because `GatingProjections <GatingProjection>` are likely to introduce cycles
(recurrent connection loops) in the graph, the effects of a GatingMechanism and its projections will generally not be
applied in the first `TRIAL` (see `initialization <System_Execution_Input_And_Initialization>` for a description of
how to configure the initialization of feedback loops in a System; also see `Scheduler` for a description of detailed
ways in which a GatingMechanism and its dependents can be scheduled to execute).

When executed, a GatingMechanism  uses its input to determine the value of its `gating_policy
<GatingMechanism.gating_policy>`, each item of which is used by a corresponding `GatingSignal` to determine its
`gating_signal <GatingSignal.gating_signal>` and assign to its `GatingProjections <GatingProjection>`. In the
subsequent `TRIAL`, each GatingProjection's value is used by the State to which it projects to modulate the `value
<State_Base.value>` of that State (see `modulation <ModulatorySignal_Modulation>` fon an explanation of how the value
of a State is modulated).

.. note::
   A State that receives a `GatingProjection` does not update its `value <State_Base.value>` (and therefore does not
   reflect the influence of its `GatingSignal`) until that State's owner Mechanism executes
   (see `Lazy Evaluation <LINK>` for an explanation of "lazy" updating).

.. _GatingMechanism_Class_Reference:

Class Reference
---------------

"""

# IMPLEMENTATION NOTE: COPIED FROM DefaultProcessingMechanism;
#                      ADD IN GENERIC CONTROL STUFF FROM DefaultGatingMechanism

import warnings

import numpy as np
import typecheck as tc

from psyneulink.core.components.functions.function import ModulationParam, _is_modulation_param
from psyneulink.core.components.mechanisms.adaptive.adaptivemechanism import AdaptiveMechanism_Base
from psyneulink.core.components.mechanisms.mechanism import Mechanism_Base
from psyneulink.core.components.states.modulatorysignals.gatingsignal import GatingSignal
from psyneulink.core.components.states.state import State_Base, _parse_state_spec
from psyneulink.core.globals.context import ContextFlags
from psyneulink.core.globals.defaults import defaultGatingPolicy
from psyneulink.core.globals.keywords import GATING, GATING_POLICY, GATING_PROJECTION, GATING_PROJECTIONS, GATING_SIGNAL, GATING_SIGNALS, GATING_SIGNAL_SPECS, INIT_EXECUTE_METHOD_ONLY, MAKE_DEFAULT_GATING_MECHANISM, OWNER_VALUE, PROJECTION_TYPE
from psyneulink.core.globals.parameters import Parameter
from psyneulink.core.globals.preferences.componentpreferenceset import is_pref_set
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel
from psyneulink.core.globals.utilities import ContentAddressableList

__all__ = [
    'GatingMechanism', 'GatingMechanismError', 'GatingMechanismRegistry'
]

GatingMechanismRegistry = {}


# MODIFIED 11/28/17 OLD:
# def _is_gating_spec(spec):
#     from psyneulink.core.components.projections.modulatory.gatingprojection import GatingProjection
#     if isinstance(spec, tuple):
#         return _is_gating_spec(spec[1])
#     elif isinstance(spec, (GatingMechanism, GatingSignal, GatingProjection)):
#         return True
#     elif isinstance(spec, type) and issubclass(spec, (GatingSignal, GatingProjection)):
#         return True
#     elif isinstance(spec, str) and spec in {GATING, GATING_PROJECTION, GATING_SIGNAL}:
#         return True
#     else:
#         return False
# MODIFIED 11/28/17 NEW:
def _is_gating_spec(spec):
    from psyneulink.core.components.projections.modulatory.gatingprojection import GatingProjection
    if isinstance(spec, tuple):
        return any(_is_gating_spec(item) for item in spec)
    if isinstance(spec, dict) and PROJECTION_TYPE in spec:
        return _is_gating_spec(spec[PROJECTION_TYPE])
    elif isinstance(spec, (GatingMechanism, GatingSignal, GatingProjection)):
        return True
    elif isinstance(spec, type) and issubclass(spec, (GatingSignal, GatingProjection, GatingMechanism)):
        return True
    elif isinstance(spec, str) and spec in {GATING, GATING_PROJECTION, GATING_SIGNAL}:
        return True
    else:
        return False
# MODIFIED 11/28/17 END


class GatingMechanismError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value


class GatingMechanism(AdaptiveMechanism_Base):
    """
    GatingMechanism(                                \
        default_gating_policy=None,                 \
        size=None,                                  \
        function=Linear(slope=1, intercept=0),      \
        gating_signals:tc.optional(list) = None,    \
        modulation=ModulationParam.MULTIPLICATIVE,  \
        params=None,                                \
        name=None,                                  \
        prefs=None)

    Subclass of `AdaptiveMechanism <AdaptiveMechanism>` that gates (modulates) the value(s)
    of one or more `States <State>`.

    COMMENT:
        Description:
            # VERIFY:
            Protocol for instantiating unassigned GatingProjections (i.e., w/o a sender specified):
               If sender is not specified for a GatingProjection (e.g., in an InputState or OutputState tuple spec)
                   it is flagged for deferred_init() in its __init__ method
               When the next GatingMechanism is instantiated, if its params[MAKE_DEFAULT_GATING_MECHANISM] == True, its
                   _take_over_as_default_gating_mechanism method is called in _instantiate_attributes_after_function;
                   it then iterates through all of the InputStates and OutputStates of all of the Mechanisms in its
                   System, identifies ones without a sender specified, calls its deferred_init() method,
                   instantiates a GatingSignal for it, and assigns it as the GatingProjection's sender.

        Class attributes:
            + componentType (str): System Default Mechanism
            + paramClassDefaults (dict):
                + FUNCTION: Linear
                + FUNCTION_PARAMS:{SLOPE:1, INTERCEPT:0}
    COMMENT

    Arguments
    ---------

    default_gating_policy : value, list or ndarray : default `defaultGatingPolicy`
        the default value for each of the GatingMechanism's GatingSignals;
        its length must equal the number of items specified in the **gating_signals** argument.

    size : int, list or 1d np.array of ints
        specifies default_gating_policy as an array of zeros if **default_gating_policy** is not passed as an
        argument;  if **default_gating_policy** is specified, it takes precedence over the specification of **size**.
        As an example, the following mechanisms are equivalent::
            T1 = TransferMechanism(size = [3, 2])
            T2 = TransferMechanism(default_variable = [[0, 0, 0], [0, 0]])

    function : TransferFunction : default Linear(slope=1, intercept=0)
        specifies the function used to transform the GatingMechanism's `variable <GatingMechanism.variable>`
        to a `gating_policy`.

    gating_signals : List[GatingSignal, InputState, OutputState, Mechanism, tuple[str, Mechanism], or dict]
        specifies the `InputStates <InputState>` and/or `OutputStates <OutputStates>`
        to be gated by the GatingMechanism; the number of items must equal the length of the **default_gating_policy**
        argument; if a `Mechanism <Mechanism>` is specified, its `primary InputState <InputState_Primary>` is used
        (see `GatingMechanism_GatingSignals for details).

    modulation : ModulationParam : ModulationParam.MULTIPLICATIVE
        specifies the default form of modulation used by the GatingMechanism's `GatingSignals <GatingSignal>`,
        unless they are `individually specified <GatingSignal_Specification>`.

    params : Dict[param keyword: param value] : default None
        a `parameter dictionary <ParameterState_Specification>` that can be used to specify the parameters
        for the Mechanism, parameters for its function, and/or a custom function and its parameters. Values
        specified for parameters in the dictionary override any assigned to those parameters in arguments of the
        constructor.

    name : str : default see `name <GatingMechanism.name>`
        specifies the name of the GatingMechanism.

    prefs : PreferenceSet or specification dict : default Mechanism.classPreferences
        specifies the `PreferenceSet` for the GatingMechanism; see `prefs <GatingMechanism.prefs>` for details.


    Attributes
    ----------

    variable : value, list or ndarray
        used as the input to the GatingMechanism's `function <GatingMechanism.function>`.  Its format is determined
        by the **default_gating_policy** or **size** argument of the GatingMechanism's constructor (see above),
        and is the same format as its `gating_policy <GatingMechanis.gating_policy>` (unless a custom
        `function <GatingMechanism.function>` has been assigned).

    function : TransferFunction
        determines the function used to transform the GatingMechanism's `variable <GatingMechanism.variable>`
        to a `gating_policy`;  the default is an identity function that simply assigns
        `variable <GatingMechanism.variable>` as the `gating_policy <GatingMechanism.gating_policy>`.

    gating_signals : ContentAddressableList[GatingSignal]
        list of `GatingSignals <GatingSignals>` for the GatingMechanism, each of which sends
        `GatingProjection(s) <GatingProjection>` to the `InputState(s) <InputState>` and/or `OutputStates <OutputState>`
        that it gates; same as GatingMechanism `output_states <Mechanism_Base.output_states>` attribute.

    gating_projections : List[GatingProjection]
        list of all of the `GatingProjections <GatingProjection>` assigned to the GatingMechanism's
        `GatingSignals <GatingSignal>` (i.e., listed in its `gating_signals <GatingMechanism.gating_signals>` attribute.

    value : scalar or 1d np.array of ints
        the result of the GatingMechanism's `function <GatingProjection.funtion>`;
        each item is the value assigned to the corresponding GatingSignal listed in `gating_signals`,
        and used by each GatingSignal to generate the `gating_signal <GatingSignal.gating_signal>` assigned to its
        `GatingProjections <GatingProjection>`;
        same as the GatingMechanism's `gating_policy <GatingMechanism.gating_policy>` attribute.
        Default is a single item used by all of the `gating_signals`.

    gating_policy : scalar or 1d np.array of ints
        the result of the GatingMechanism's `function <GatingProjection.function>`;
        each item is the value assigned to the corresponding GatingSignal listed in `gating_signals`,
        and used by each GatingSignal to generate the `gating_signal <GatingSignal.gating_signal>` assigned to its
        `GatingProjections <GatingProjection>`; same as the GatingMechanism's `value <GatingMechanism.value>` attribute.
        Default is a single item used by all of the `gating_signals`.


    modulation : ModulationParam
        the default form of modulation used by the GatingMechanism's `GatingSignals <GatingSignal>`,
        unless they are `individually specified <GatingSignal_Specification>`.

    name : str
        the name of the GatingMechanism; if it is not specified in the **name** argument of the constructor, a
        default is assigned by MechanismRegistry (see `Naming` for conventions used for default and duplicate names).

    prefs : PreferenceSet or specification dict
        the `PreferenceSet` for the GatingMechanism; if it is not specified in the **prefs** argument of the
        constructor, a default is assigned using `classPreferences` defined in __init__.py (see :doc:`PreferenceSet
        <LINK>` for details).
    """

    componentType = "GatingMechanism"

    initMethod = INIT_EXECUTE_METHOD_ONLY

    outputStateType = GatingSignal

    stateListAttr = Mechanism_Base.stateListAttr.copy()
    stateListAttr.update({GatingSignal:GATING_SIGNALS})


    classPreferenceLevel = PreferenceLevel.TYPE
    # Any preferences specified below will override those specified in TypeDefaultPreferences
    # Note: only need to specify setting;  level will be assigned to TYPE automatically
    # classPreferences = {
    #     kwPreferenceSetName: 'GatingMechanismClassPreferences',
    #     kp<pref>: <setting>...}

    class Parameters(AdaptiveMechanism_Base.Parameters):
        """
            Attributes
            ----------

                variable
                    see `variable <GatingMechanism.variable>`

                    :default value: numpy.array([0.5])
                    :type: numpy.ndarray

                value
                    see `value <GatingMechanism.value>`

                    :default value: numpy.array([[0]])
                    :type: numpy.ndarray

        """
        # This must be a list, as there may be more than one (e.g., one per GATING_SIGNAL)
        variable = np.array(defaultGatingPolicy)
        value = Parameter(AdaptiveMechanism_Base.Parameters.value.default_value, aliases=['gating_policy'])

    paramClassDefaults = Mechanism_Base.paramClassDefaults.copy()
    paramClassDefaults.update({GATING_PROJECTIONS: None})

    @tc.typecheck
    def __init__(self,
                 default_gating_policy=None,
                 size=None,
                 function=None,
                 gating_signals:tc.optional(list) = None,
                 modulation:tc.optional(_is_modulation_param)=ModulationParam.MULTIPLICATIVE,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None):

        # self.system = None

        # Assign args to params and functionParams dicts
        params = self._assign_args_to_param_dicts(gating_signals=gating_signals,
                                                  function=function,
                                                  params=params)

        super().__init__(default_variable=default_gating_policy,
                         size=size,
                         modulation=modulation,
                         function=function,
                         params=params,
                         name=name,
                         prefs=prefs,
                         context=ContextFlags.CONSTRUCTOR)

    def _validate_params(self, request_set, target_set=None, context=None):
        """Validate items in the GATING_SIGNALS param (**gating_signals** argument of constructor)

        Check that GATING_SIGNALS is a list, and that every item is valid state_spec
        """

        super(GatingMechanism, self)._validate_params(request_set=request_set,
                                                      target_set=target_set,
                                                      context=context)

        if GATING_SIGNALS in target_set and target_set[GATING_SIGNALS]:
            if not isinstance(target_set[GATING_SIGNALS], list):
                target_set[g] = [target_set[GATING_SIGNALS]]
            for gating_signal in target_set[GATING_SIGNALS]:
                _parse_state_spec(state_type=GatingSignal, owner=self, state_spec=gating_signal)

    def _instantiate_output_states(self, context=None):

        from psyneulink.core.globals.registry import register_category

        # Create registry for GatingSignals (to manage names)

        register_category(entry=GatingSignal,
                          base_class=State_Base,
                          registry=self._stateRegistry,
                          context=context)

        if self.gating_signals:

            self._output_states = []

            for gating_signal in self.gating_signals:
                self._instantiate_gating_signal(gating_signal, context=context)

        super()._instantiate_output_states(context=context)

        # Reassign gating_signals to capture any user_defined GatingSignals instantiated in call to super
        #    and assign to ContentAddressableList
        self._gating_signals = ContentAddressableList(component_type=GatingSignal,
                                                      list=[state for state in self.output_states
                                                            if isinstance(state, GatingSignal)])

        # If the GatingMechanism's policy has more than one item,
        #    warn if the number of items does not equal the number of its GatingSignals
        #    (note:  there must be fewer GatingSignals than items in gating_policy,
        #            as the reverse is an error that is checked for in _instantiate_gating_signal)
        if len(self.gating_policy)>1 and len(self.gating_signals) != len(self.gating_policy):
            if self.verbosePref:
                warnings.warning("The number of {}s for {} ({}) does not equal the number of items in its {} ({})".
                                 format(GatingSignal.__name__, self.name, len(self.gating_signals),
                                        GATING_POLICY, len(self.gating_policy)))

    def _instantiate_gating_signal(self, gating_signal, context=None):
        """Instantiate GatingSignal OutputState and assign (if specified) or instantiate GatingProjection

        Notes:
        * gating_signal arg can be a:
            - GatingSignal object;
            - GatingProjection;
            - InputState or OutputState;
            - params dict, from _take_over_as_default_gating_mechanism(), containing a GatingProjection;
            - tuple (state_name, Mechanism), from gating_signals arg of constructor;
                    [NOTE: this is a convenience format;
                           it precludes specification of GatingSignal params (e.g., MODULATION_OPERARATION)]
            - GatingSignal specification dictionary, from gating_signals arg of constructor
                    [NOTE: this must have at least NAME:str (state name) and MECHANISM:Mechanism entries;
                           it can also include a PARAMS entry with a params dict containing GatingSignal params]
        * State._parse_state_spec() is used to parse gating_signal arg
        * params are expected to be for (i.e., to be passed to) GatingSignal;
        * wait to instantiate deferred_init() projections until after GatingSignal is instantiated,
            so that correct OutputState can be assigned as its sender
        # * index of OutputState is incremented based on number of GatingSignals already instantiated;
        #     this means that the GatingMechanism's function must return as many items as it has GatingSignals,
        #     with each item of the function's value used by a corresponding GatingSignal.
            Note: multiple GatingProjections can be assigned to the same GatingSignal to achieve "divergent gating"
                  (that is, gating of many states with a single value -- e.g., LC)
        * index of OutputState is assigned to [0], so that all GatingSignals use the same single value produced
            returned by a GatingMechanism's function

        Returns GatingSignal (OutputState)
        """
        from psyneulink.core.components.states.state import _instantiate_state

        # Parse gating_signal specifications (in call to State._parse_state_spec)
        #    and any embedded Projection specifications (in call to <State>._instantiate_projections)
        # KDM 5/29/18: here, what happens if you make two gating signals with the same owner (self)?
        # looks like they both will get the variable spec (OWNER_VALUE, 0)
        gating_signal = _instantiate_state(state_type=GatingSignal,
                                           variable=(OWNER_VALUE,0),
                                           owner=self,
                                           reference_value=defaultGatingPolicy,
                                           modulation=self.modulation,
                                           state_spec=gating_signal,
                                           context=context)

        # Validate index
        try:
            self.gating_policy[gating_signal.owner_value_index]
        except IndexError:
            raise GatingMechanismError("Index specified for {} of {} ({}) "
                                       "exceeds the number of items of its {} ({})".
                                       format(GatingSignal.__name__, self.name, gating_signal.owner_value_index,
                                              GATING_POLICY, len(self.gating_policy)))

        # Add GatingSignal TO output_states LIST
        self._output_states.append(gating_signal)

        # Add GatingProjection(s) to GatingMechanism's list of GatingProjections
        try:
            self.gating_projections.extend(gating_signal.efferents)
        except AttributeError:
            self.gating_projections = gating_signal.efferents.copy()

        return gating_signal

    def _instantiate_attributes_after_function(self, context=None):
        """Take over as default GatingMechanism (if specified) and implement any specified GatingProjections
        """

        super()._instantiate_attributes_after_function(context=context)

        if MAKE_DEFAULT_GATING_MECHANISM in self.paramsCurrent:
            if self.paramsCurrent[MAKE_DEFAULT_GATING_MECHANISM]:
                self._assign_as_gating_mechanism(context=context)

        # FIX: 5/23/17 CONSOLIDATE/SIMPLIFY THIS RE: gating_signal ARG??  USE OF PROJECTIONS, ETC.
        # FIX:         ?? WHERE WOULD GATING_PROJECTIONS HAVE BEEN SPECIFIED IN paramsCURRENT??
        # FIX:         DOCUMENT THAT VALUE OF GATING ENTRY CAN BE A PROJECTION
        # FIX:         RE-WRITE parse_state_spec TO TAKE TUPLE THAT SPECIFIES (PARAM VALUE, GATING SIGNAL)
        #                       RATHER THAN (PARAM VALUE, GATING PROJECTION)
        # FIX: NOT CLEAR THIS IS GETTING USED AT ALL; ALSO, ??REDUNDANT WITH CALL IN _instantiate_output_states
        # If GatingProjections were specified, implement them
        if GATING_PROJECTIONS in self.paramsCurrent:
            if self.paramsCurrent[GATING_PROJECTIONS]:
                for key, projection in self.paramsCurrent[GATING_PROJECTIONS].items():
                    self._instantiate_gating_projection(projection, context=ContextFlags.METHOD)

    def _assign_as_gating_mechanism(self, context=None):

        # FIX 5/23/17: INTEGRATE THIS WITH ASSIGNMENT OF gating_signals
        # FIX:         (E.G., CHECK IF SPECIFIED GatingSignal ALREADY EXISTS)
        # Check the input_states and output_states of the System's Mechanisms
        #    for any GatingProjections with deferred_init()
        for mech in self.system.mechanisms:
            for state in mech._input_states + mech._output_states:
                for projection in state.mod_afferents:
                    # If projection was deferred for init, initialize it now and instantiate for self
                    if (projection.context.initialization_status == ContextFlags.DEFERRED_INIT
                        and projection.init_args['sender'] is None):
                        # FIX 5/23/17: MODIFY THIS WHEN (param, GatingProjection) tuple
                        # FIX:         IS REPLACED WITH (param, GatingSignal) tuple
                        # Add projection itself to any params specified in the GatingProjection for the GatingSignal
                        #    (cached in the GatingProjection's gating_signal attrib)
                        gating_signal_specs = projection.gating_signal or {}
                        gating_signal_specs.update({GATING_SIGNAL_SPECS: [projection]})
                        self._instantiate_gating_signal(gating_signal_specs, context=context)

        self._activate_projections_for_compositions(self.system)

    def _activate_projections_for_compositions(self, compositions=None):
        for gp in self.gating_signals:
            for eff in gp.efferents:
                eff._activate_for_compositions(compositions)

    def show(self):
        """Display the InputStates and/or OutputStates gated by the GatingMechanism's `gating_signals
        <GatingMechanism.gating_signals>`.
        """

        print ("\n---------------------------------------------------------")

        print ("\n{0}".format(self.name))
        print ("\n\tGating the following Mechanism InputStates and/or OutputStates:".format(self.name))
        # Sort for consistency of output:
        state_names_sorted = sorted(self.output_states)
        for state_name in state_names_sorted:
            for projection in self.output_states[state_name].efferents:
                print ("\t\t{0}: {1}".format(projection.receiver.owner.name, projection.receiver.name))
        print ("\n---------------------------------------------------------")


# IMPLEMENTATION NOTE:  THIS SHOULD BE MOVED TO COMPOSITION ONCE THAT IS IMPLEMENTED
def _add_gating_mechanism_to_system(owner:GatingMechanism):

    if owner.gating_signals:
        for gating_signal in owner.gating_signals:
            for mech in [proj.receiver.owner for proj in gating_signal.efferents]:
                for system in mech.systems:
                    if owner not in system.execution_list:
                        system.execution_list.append(owner)
                        system.execution_graph[owner] = set()
                        # FIX: NEED TO ALSO ADD SystemInputState (AND ??ProcessInputState) PROJECTIONS
                        # # Add self to system's list of OriginMechanisms if it doesn't have any afferents
                        # if not any(state.path_afferents for state in owner.input_states):
                        #     system.origin_mechanisms.mechs.append(owner)



# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# ********************************************  ModulatorySignal *******************************************************

"""
Overview
--------

A ModulatorySignal is a subclass of `OutputState` that belongs to an `AdaptiveMechanism <AdaptiveMechanism>`, and is
used to `modulate <ModulatorySignal_Modulation>` the `value <State_Base.value>` of one or more `States <State>` by way
of one or more `ModulatoryProjections <ModulatoryProjection>` (see `ModulatorySignal_Naming` for conventions on how
modulatory components are named). A ModulatorySignal modulates the value of a State by modifying a parameter of the
State's `function <State_Base.function>`.  There are three types of ModulatorySignals, each of which is  associated with
a particular type of `AdaptiveMechanism <AdaptiveMechanism>` and `ModulatoryProjection <ModulatoryProjection>`, and
modifies the value of a different type of State, as described below (and shown in the
`figure <ModulatorySignal_Anatomy_Figure>`):

* `LearningSignal`
    takes the `value <LearningSignal.value>` assigned to it by the `LearningMechanism` to which it belongs,
    and uses it to modulate the parameter of a `PathwayProjection <PathwayProjection>` -- usually the `matrix
    <MappingProjection.matrix>` parameter of a `MappingProjection`.
..
* `ControlSignal`
    takes the `value <ControlSignal.value>` assigned to it by the `ControlMechanism <ControlMechanism>` to which it
    belongs, and uses it to modulate the parameter of a `Mechanism <Mechanism>` or its `function
    <Mechanism_Base.function>`.
..
* `GatingSignal`
    takes the `value <GatingSignal.value>` assigned to it by the `GatingMechanism` to which it belongs,
    and uses it to modulate the value of the `InputState` or `OutputState` of a `Mechanism <Mechanism>`.

.. _ModulatorySignal_Naming:

Modulatory Components and their attributes are named according to the category of modulation:

    - AdaptiveMechanism name: <*Category*>Mechanism (e.g., ControlMechanism)
    - ModulatorySignal name: <*Category*>Signal (e.g., ControlSignal)
    - ModulatoryProjection name: <*Category*>Projection (e.g., ControlProjection)
    - List of an AdaptiveMechanism's ModulatorySignals: <*CategoryMechanism*>.category_signals
      (e.g., ControlMechanism.control_signals)
    - Value of a ModulatorySignal: <*CategorySignal*>.category_signal (e.g., ControlSignal.control_signal)


.. _ModulatorySignal_Creation:

Creating a ModulatorySignal
---------------------------

A ModulatorySignal is a base class, and cannot be instantiated directly.  However, the three types of ModulatorySignals
listed above can be created directly, by calling the constructor for the desired type.  More commonly, however,
ModulatorySignals are created automatically by the `AdaptiveMechanism <AdaptiveMechanism>` to which they belong, or by
specifying them in the constructor for an `AdaptiveMechanism <AdaptiveMechanism>` (the details of which are described in
the documentation for each type of ModulatorySignal).

.. _ModulatorySignal_Structure:

Structure
---------

A ModulatorySignal is associated with one or more `ModulatoryProjections <ModulatoryProjection>` of the
corresponding type, that project to the State(s), the value(s) of which it modulates.  The ModulatoryProjections
received by a `State <State>` are listed in its `mod_afferents` attribute. The method by which a ModulatorySignal
modulates a State's `value <State_Base.value>` is determined by the ModulatorySignal's
`modulation <ModulatorySignal.modulation>` attribute, as described below.

COMMENT:
    ADD ADDITIONAL NOTE HERE ABOUT THE USE OF MULTIPE ModulatorySignals IN A SINGLE AdapativeMechanism VS.
    MULTIPLE ModulatoryProjections FOR A SINGLE ModulatorySignal (AS DESCRIBED BELOW).
COMMENT

.. _ModulatorySignal_Projections:

*Projections*
~~~~~~~~~~~~~

A ModulatorySignal can be assigned one or more `ModulatoryProjections <ModulatoryProjection>`,
using either the **projections** argument of its constructor, or in an entry of a dictionary assigned to the
**params** argument with the key *PROJECTIONS*.  These are assigned to its `efferents  <ModulatorySignal.efferents>`
attribute.  See `State Projections <State_Projections>` for additional details concerning the specification of
Projections when creating a State.

.. note::
   Although a ModulatorySignal can be assigned more than one `ModulatoryProjection <ModulatoryProjection>`, all of those
   Projections receive and convey the same modulatory value (received from the `AdaptiveMechanism
   <AdaptiveMechanism>` to which the ModulatorySignal belongs), and use the same form of `modulation
   <ModulatorySignal_Modulation>`.  This is a common use for some ModulatorySignals (e.g., the use of a single
   `GatingSignal` to gate multiple `InputState(s) <InputState>` or `OutputState(s) <OutputState>`), but requires more
   specialized circumstances for others (e.g., the use of a single `LearningSignal` for more than one
   `MappingProjection`, or a single `ControlSignal` for the parameters of more than one Mechanism).

.. _ModulatorySignal_Execution:


.. _ModulatorySignal_Modulation:

*Modulation*
~~~~~~~~~~~~

A ModulatorySignal modulates the value of a `State <State>` either by modifying a parameter of the State's `function
<State_Base.function>` (which determines the State's `value <State_Base.value>`), or by assigning a value to the State
directly.

The `function <State_Base.function>` of every State designates one of its parameters as its
*MULTIPLICATIVE_PARAM* and another as its *ADDITIVE_PARAM*;  some may also designate other modulatory parameters. The
`modulation <ModulatorySignal.modulation>` attribute of a ModulatorySignal determines which of these parameters
are assigned its value, or which of two other actions to take when the State updates its `value <State_Base.value>`.
It is specified using a value of `ModulationParam <Function.ModulationParam>`.

The default for `ControlSignals <ControlSignal>` and `GatingSignals <GatingSignal>` is `ModulationParam.MULTIPLICATIVE`,
which multiplicatively modifies the State's `variable <State_Base.variable>` by the `value <ModulatorySignal>` of the
ModulatorySignal before passing it to the State's `function <State_Base.function>`.  The default for `LearningSignals
<LearningSignal>` is `ModulationParam.ADDITIVE`, which additively modifies the `value <LearningSignal.value>` of the
LearningSignal (i.e., the weight changes computed by the `LearningMechanism`) to the State's `variable
<State_Base.variable>` (i.e., the current weight `matrix <MappingProjection.matrix>` for the `MappingProjection` being
learned).

The `modulation <ModulatorySignal.modulation>` attribute can be specified in the **modulation** argument of the
ModulatorySignal's constructor, or in a *MODULATION* entry of a `State specification dictionary <State_Specification>`
used to create the ModulatorySignal. If it is not specified when a ModulatorySignal is created, it is assigned the value
of the `modulation <AdaptiveMechanism_Base.modulation>` attribute for the `AdaptiveMechanism <AdaptiveMechanism>` to
which it belongs.

.. note::
   `OVERRIDE <ModulatorySignal_Modulation>` can be specified for **only one** ModulatoryProjection to a State;
   specifying it for more than one causes an error.


.. _ModulatorySignal_Anatomy_Figure:

**Anatomy of Modulation**

.. figure:: _static/Modulation_fig.svg
   :alt: Modulation
   :scale: 150 %

   **Three types of Modulatory Components and the States they modulate**.
   The table below lists the default `ModulatoryParam` for each type of ModulatorySignal, and the default Function
   and modulated parameter of its recipient State.  The figure shows a detailed view of how ModulatorySignals
   modulate the parameters of a State's `function <State_Base.function>`.

   .. table:: **ModulatorySignals and States they Modulate**
      :align: left

      +--------------------+-----------------------+--------------------------------------+----------------------------+
      |     Modulatory     |Default ModulationParam|                                      |Default Function (mod param)|
      |     Component      |for ModulatorySignal   |           Recipient State            |for Recipient State         |
      +====================+=======================+======================================+============================+
      | **Control** (blue) |   *MULTIPLICATIVE*    | Mechanism `ParameterState`           | `Linear` (`slope`)         |
      +--------------------+-----------------------+--------------------------------------+----------------------------+
      | **Gating** (brown) |   *MULTIPLICATIVE*    | Mechanism `InputState`/`OutputState` | `Linear` (`slope`)         |
      +--------------------+-----------------------+--------------------------------------+----------------------------+
      |**Learning** (green)|     *ADDITIVE*        | MappingProjection `ParameterState`   | `AccumulatorIntegrator`    |
      |                    |                       |                                      | (`increment`)              |
      +--------------------+-----------------------+--------------------------------------+----------------------------+

.. _ModulatorySignal_Detail_Figure:

**Detailed View of Modulation**

.. figure:: _static/Modulation_Detail_fig.svg
   :alt: Modulation_Detail
   :scale: 150 %

   How a ModulatorySignal signal influences the value of a State is determined by its
   `modulation <ModulatorySignal.modulation>` attribute, which is specified as a value of `ModulationParam`:
   *ADDITIVE* and *MULTIPLICATIVE* specify that the `value <ModulatorySignal.value>` of the ModulatorySignal
   be assigned to the correspondingly designated parameter of the State's function;  *OVERRIDE* specifies
   that the ModulatorySignal's `value <ModulatorySignal.value>` be assigned directly as the State's
   `value <State_Base.value>`, in effect ignoring the State's `variable <State_Base.variable>` and
   `function <State_Base.function>`.

Execution
---------

ModulatorySignals cannot be executed.  They are updated when the `AdaptiveMechanism <AdaptiveMechanism>` to which they
belong is executed. When a ModulatorySignal is updated, it calculates its value, which is then made available to the
`ModulatoryProjections <ModulatoryProjection>` listed in its `efferents <ModulatorySignal.efferents>` attribute.
When those Projections execute, they convey the ModulatorySignal's `value <ModulatorySignal.value>` to the
`function <State_Base.function>` of the `State <State>` to which they project.  The State's `function
<State_Base.function>` then uses that value for the parameter designated by the `modulation
<ModulatorySignal.modulation>` attribute of the ModulatorySignal when the State is updated.

For example, consider a `ControlSignal` that modulates the `bias f<Logistic.bias>` parameter of a `Logistic` Function
used by a `TransferMechanism, and assume that the `ParameterState` for the bias parameter (to which the ControlSignal
projects) uses a `Linear` function to update its value (which is the default for a ParameterState).  If the
`modulation  <ModulatorySignal.modulation>` attribute of the `ControlSignal` is `ModulationParam.MULTIPLICATIVE`,
then it will be assigned to the `slope <Linear>` parameter of the ParameterState's `function <ParameterState.function>`.
Accordingly, when the ParameterState is updated it will multiply the bias parameter's value by the value of the
ControlSignal to determine the value of the bias parameter.  The result will used as the value of the bias for the
Logistic Function when the TransferMechanism is executed (see `State_Execution` for additional details).

.. note::
   The change in the value of a `State <State>` in response to a ModulatorySignal does not occur until the Mechanism to
   which the state belongs is next executed; see :ref:`Lazy Evaluation <LINK>` for an explanation of "lazy" updating).

.. _ModulatorySignal_Class_Reference:

Class Reference
---------------
"""

from psyneulink.core.components.component import component_keywords
from psyneulink.core.components.states.outputstate import OutputState
from psyneulink.core.components.states.state import State_Base
from psyneulink.core.globals.context import ContextFlags
from psyneulink.core.globals.keywords import MECHANISM, MODULATION, MODULATORY_SIGNAL
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel

__all__ = [
    'modulatory_signal_keywords', 'ModulatorySignal', 'ModulatorySignalError',
]


def _is_modulatory_spec(spec, include_matrix_spec=True):
    from psyneulink.core.components.mechanisms.adaptive.learning.learningmechanism import _is_learning_spec
    from psyneulink.core.components.mechanisms.adaptive.control.controlmechanism import _is_control_spec
    from psyneulink.core.components.mechanisms.adaptive.gating.gatingmechanism import _is_gating_spec

    if (_is_learning_spec(spec, include_matrix_spec=include_matrix_spec)
        or _is_control_spec(spec)
        or _is_gating_spec(spec)
        ):
        return True
    else:
        return False


class ModulatorySignalError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)

modulatory_signal_keywords = {MECHANISM, MODULATION}
modulatory_signal_keywords.update(component_keywords)


class ModulatorySignal(OutputState):
    """
    ModulatorySignal(                               \
        owner,                                      \
        function=LinearCombination(operation=SUM),  \
        modulation=ModulationParam.MULTIPLICATIVE   \
        projections=None,                           \
        params=None,                                \
        name=None,                                  \
        prefs=None)

    Subclass of `OutputState` used by an `AdaptiveMechanism <AdaptiveMechanism>` to modulate the value
    of one more `States <State>`.

    .. note::
       ModulatorySignal is an abstract class and should NEVER be instantiated by a call to its constructor.
       It should be instantiated using the constructor for a `subclass <ModulatorySignal_Subtypes>`.

    COMMENT:

        Description
        -----------
            The ModulatorySignal class is a subtype of the OutputState class in the State category of Component,
            It is used primarily as the sender for GatingProjections
            Its FUNCTION updates its value:
                note:  currently, this is the identity function, that simply maps variable to self.value

        Class attributes:
            + componentType (str) = GATING_SIGNAL
            + paramClassDefaults (dict)
                + FUNCTION (LinearCombination)
                + FUNCTION_PARAMS (Modulation.MULTIPLY)

        Class methods:
            function (executes function specified in params[FUNCTION];  default: Linear

        StateRegistry
        -------------
            All OutputStates are registered in StateRegistry, which maintains an entry for the subclass,
              a count for all instances of it, and a dictionary of those instances
    COMMENT


    Arguments
    ---------

    owner : GatingMechanism
        specifies the `GatingMechanism` to which to assign the ModulatorySignal.

    function : Function or method : default Linear
        specifies the function used to determine the value of the ModulatorySignal from the value of its
        `owner <GatingMechanism.owner>`.

    modulation : ModulationParam : default ModulationParam.MULTIPLICATIVE
        specifies the type of modulation the ModulatorySignal uses to determine the value of the State(s) it modulates.

    params : Dict[param keyword: param value] : default None
        a `parameter dictionary <ParameterState_Specification>` that can be used to specify the parameters for
        the ControlSignal and/or a custom function and its parameters. Values specified for parameters in the dictionary
        override any assigned to those parameters in arguments of the constructor.

    name : str : default see `name <ModulatorySignal.name>`
        specifies the name of the ModulatorySignal.

    prefs : PreferenceSet or specification dict : default State.classPreferences
        specifies the `PreferenceSet` for the LearningSignal; see `prefs <ControlSignal.prefs>` for details.


    Attributes
    ----------

    owner : AdaptiveMechanism
        the `AdaptiveMechanism <AdaptiveMechanism>` to which the ModulatorySignal belongs.

    variable : number, list or np.ndarray
        value assigned by the ModulatorySignal's `owner <ModulatorySignal.owner>`, and used by the ModulatorySignal's
        `function <ModulatorySignal.function>` to compute its `value <ModulatorySignal.value>`.

    function : TransferFunction :  default Linear(slope=1, intercept=0)
        provides the ModulatorySignal's `value <ModulatorySignal.value>`; the default is an identity function that
        assigns `variable <ModulatorySignal.variable>` as ModulatorySignal's `value <ModulatorySignal.value>`.

    value : number, list or np.ndarray
        result of `function <ModulatorySignal.function>`, used to determine the `value <State_Base.value>` of the
        State(s) being modulated.

    modulation : ModulationParam
        determines how the output of the ModulatorySignal is used to modulate the value of the state(s) being modulated.

    efferents : [List[GatingProjection]]
        a list of the `ModulatoryProjections <ModulatoryProjection>` assigned to the ModulatorySignal.

    name : str
        the name of the ModulatorySignal. If the ModulatorySignal's `initialization has been deferred
        <State_Deferred_Initialization>`, it is assigned a temporary name (indicating its deferred initialization
        status) until initialization is completed, at which time it is assigned its designated name.  If that is the
        name of an existing ModulatorySignal, it is appended with an indexed suffix, incremented for each State with
        the same base name (see `Naming`). If the name is not  specified in the **name** argument of its constructor,
        a default name is assigned as follows; if the ModulatorySignal has:

        * no projections (which are used to name it) -- the name of its class is used, with an index that is
        incremented for each ModulatorySignal with a default named assigned to its `owner <ModulatorySignal.owner>`;

        * one `ModulatoryProjection` -- the following template is used:
          "<target Mechanism name> <target State name> <ModulatorySignal type name>"
          (for example, ``'Decision[drift_rate] ControlSignal'``, or ``'Input Layer[InputState-0] GatingSignal'``);

        * multiple ModulatoryProjections, all to States of the same Mechanism -- the following template is used:
          "<target Mechanism name> (<target State name>,...) <ModulatorySignal type name>"
          (for example, ``Decision (drift_rate, threshold) ControlSignal``, or
          ``'Input Layer[InputState-0, InputState-1] GatingSignal'``);

        * multiple ModulatoryProjections to States of different Mechanisms -- the following template is used:
          "<owner Mechanism's name> divergent <ModulatorySignal type name>"
          (for example, ``'ControlMechanism divergent ControlSignal'`` or ``'GatingMechanism divergent GatingSignal'``).

        .. note::
            Unlike other PsyNeuLink components, State names are "scoped" within a Mechanism, meaning that States with
            the same name are permitted in different Mechanisms.  However, they are *not* permitted in the same
            Mechanism: States within a Mechanism with the same base name are appended an index in the order of their
            creation.

    prefs : PreferenceSet or specification dict
        the `PreferenceSet` for the ModulatorySignal; if it is not specified in the **prefs** argument of the
        constructor, a default is assigned using `classPreferences` defined in __init__.py (see :doc:`PreferenceSet
        <LINK>` for details).

    """

    componentType = MODULATORY_SIGNAL
    # paramsType = OUTPUT_STATE_PARAMS

    class Parameters(OutputState.Parameters):
        """
            Attributes
            ----------

                modulation
                    see `modulation <ModulatorySignal.modulation>`

                    :default value: None
                    :type:

        """
        modulation = None

    stateAttributes =  OutputState.stateAttributes | {MODULATION}

    classPreferenceLevel = PreferenceLevel.TYPE
    # Any preferences specified below will override those specified in TypeDefaultPreferences
    # Note: only need to specify setting;  level will be assigned to TYPE automatically
    # classPreferences = {
    #     kwPreferenceSetName: 'OutputStateCustomClassPreferences',
    #     kp<pref>: <setting>...}

    paramClassDefaults = State_Base.paramClassDefaults.copy()

    def __init__(self,
                 owner=None,
                 size=None,
                 reference_value=None,
                 variable=None,
                 projections=None,
                 modulation=None,
                 index=None,
                 assign=None,
                 params=None,
                 name=None,
                 prefs=None,
                 context=None,
                 function=None,
                 ):

        # Deferred initialization
        # if self.context.initialization_status & (ContextFlags.DEFERRED_INIT | ContextFlags.INITIALIZING):
        if self.context.initialization_status & ContextFlags.DEFERRED_INIT:
            # If init was deferred, it may have been because owner was not yet known (see OutputState.__init__),
            #   and so modulation hasn't had a chance to be assigned to the owner's value
            #   (i.e., if it was not specified in the constructor), so do it now;
            #   however modulation has already been assigned to params, so need to assign it there
            params[MODULATION] = self.modulation or owner.modulation

        # Standard initialization
        else:
            # Assign args to params and functionParams dicts 
            params = self._assign_args_to_param_dicts(params=params,
                                                      modulation=modulation)

        super().__init__(owner=owner,
                         reference_value=reference_value,
                         variable=variable,
                         size=size,
                         projections=projections,
                         index=index,
                         assign=assign,
                         params=params,
                         name=name,
                         prefs=prefs,
                         context=context,
                         function=function,
                         )

        if self.context.initialization_status == ContextFlags.INITIALIZED:
            self._assign_default_state_name(context=context)

    def _instantiate_attributes_after_function(self, context=None):
        # If owner is specified but modulation has not been specified, assign to owner's value

        super()._instantiate_attributes_after_function(context=context)
        if self.owner and self.modulation is None:
            self.modulation = self.owner.modulation


    def _instantiate_projections(self, projections, context=None):
        """Instantiate Projections specified in PROJECTIONS entry of params arg of State's constructor

        Specification should be an existing ModulatoryProjection, or a receiver Mechanism or State
        Disallow any other specifications (including PathwayProjections)
        Call _instantiate_projection_from_state to assign ModulatoryProjections to .efferents

        """
       # # IMPLEMENTATION NOTE: THIS SHOULD BE MOVED TO COMPOSITION ONCE THAT IS IMPLEMENTED
        for receiver_spec in projections:
            projection = self._instantiate_projection_from_state(projection_spec=type(self),
                                                                 receiver=receiver_spec,
                                                                 context=context)
            projection._assign_default_projection_name(state=self)

    def _assign_default_state_name(self, context=None):

        # If the name is not a default name for the class,
        #    or the ModulatorySignal has no projections (which are used to name it)
        #    then return
        if (not (self.name is self.__class__.__name__
                 or self.__class__.__name__ + '-' in self.name) or
                    len(self.efferents)==0):
            return self.name

        # Construct default name
        receiver_names = []
        receiver_owner_names = []
        receiver_owner_receiver_names = []
        class_name = self.__class__.__name__

        for projection in self.efferents:
            receiver = projection.receiver
            receiver_name = receiver.name
            receiver_owner_name = receiver.owner.name
            receiver_names.append(receiver_name)
            receiver_owner_names.append(receiver_owner_name)
            receiver_owner_receiver_names.append("{}[{}]".format(receiver_owner_name, receiver_name))

        # Only one ModulatoryProjection: "<target mech> <State.name> <ModulatorySignal>"
        # (e.g., "Decision drift_rate ControlSignal", or "Input Layer InputState-0 GatingSignal")
        if len(receiver_owner_receiver_names) == 1:
            default_name = receiver_owner_receiver_names[0] + " " + class_name

        # Multiple ModulatoryProjections all for same mech: "<target mech> (<State.name>,...) <ModulatorySignal>"
        # (e.g., "Decision (drift_rate, threshold) ControlSignal" or
        #        "InputLayer (InputState-0, InputState-0) ControlSignal")
        elif all(name is receiver_owner_names[0] for name in receiver_owner_names):
            default_name = "{}[{}] {}".format(receiver_owner_names[0], ", ".join(receiver_names), class_name)

        # Mult ModulatoryProjections for diff mechs: "<owner mech> divergent <ModulatorySignal>"
        # (e.g., "EVC divergent ControlSignal", or "GatingMechanism divergent GatingSignal")
        else:
            default_name = self.name + " divergent " + class_name

        self.name = default_name

        return self.name

import streamlit as st
import pandas as pd
import numpy as np
from calculators.simple_calc.simple_calc import SimpleCalc

# calc = SimpleCalc()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    # First Section: Preindustrial given Pre-Equilibrium

    if 'preindustrial_given_pre_equilibrium' not in st.session_state:
        st.session_state.preindustrial_given_pre_equilibrium = 0.5

    def update_preequilibrium_from_slider():
        st.session_state.preindustrial_given_pre_equilibrium = st.session_state['pre_equilibrium_slider_value']

    def update_preindustrial_from_number():
        st.session_state.preindustrial_given_pre_equilibrium = st.session_state['pre_equilibrium_num_input_value']

    st.slider(
        label='Preindustrial given Pre-Equilibrium',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.preindustrial_given_pre_equilibrium,
        step=0.001,
        format="%f",
        on_change=update_preequilibrium_from_slider,
        key='pre_equilibrium_slider_value')

    st.number_input(label='Preindustrial (Number) given pre-equilibrium',
                    value=st.session_state.preindustrial_given_pre_equilibrium,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.001,
                    format="%f",
                    on_change=update_preindustrial_from_number,
                    key='pre_equilibrium_num_input_value')

    st.slider(label='Extinction given Pre-Equilibrium',
            min_value=0.0,
            max_value=1.0,
            value=1 - st.session_state.preindustrial_given_pre_equilibrium,
            disabled=True, format="%f")


# Second Section: Industrial given Preindustrial

with col2:

    if 'industrial_given_preindustrial' not in st.session_state:
        st.session_state.industrial_given_preindustrial = 0.5

    def update_preindustrial_from_slider():
        st.session_state.industrial_given_preindustrial = st.session_state['preindustrial_slider_value']

    def update_preindustrial_from_number():
        st.session_state.industrial_given_preindustrial = st.session_state['preindustrial_num_input_value']

    st.slider(
        label='Industrial (Slider) given Preindustrial',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.industrial_given_preindustrial,
        step=0.001,
        format="%f",
        on_change=update_preindustrial_from_slider,
        key='preindustrial_slider_value')

    st.number_input(label='Industrial (Number) given Preindustrial',
                    value=st.session_state.industrial_given_preindustrial,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.001,
                    format="%f",
                    on_change=update_preindustrial_from_number,
                    key='preindustrial_num_input_value')

    st.slider(label='Extinction given Preindustrial',
            min_value=0.0,
            max_value=1.0,
            value=1 - st.session_state.industrial_given_preindustrial,
            disabled=True, format="%f")


# Third Section: Future perils given preindustrial

with col3:

    if 'future_perils_given_industrial' not in st.session_state:
        st.session_state.future_perils_given_industrial = 0.5

    def update_perils_from_slider():
        st.session_state.future_perils_given_industrial = st.session_state['future_perils_slider_value']

    def update_perils_from_number():
        st.session_state.future_perils_given_industrial = st.session_state['future_perils_num_input_value']

    st.slider(
        label='Future perils (slider) given industrial',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.future_perils_given_industrial,
        step=0.001,
        format="%f",
        on_change=update_perils_from_slider,
        key='future_perils_slider_value')

    st.number_input(label='Future perils (number) given industrial',
                    value=st.session_state.future_perils_given_industrial,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.001,
                    format="%f",
                    on_change=update_perils_from_number,
                    key='future_perils_num_input_value')

    st.slider(label='Extinction given industrial',
            min_value=0.0,
            max_value=1.0,
            value=1 - st.session_state.future_perils_given_industrial,
            disabled=True, format="%f")





# # Section 4: Transitions from present perils

'---'

st.markdown("""## Transitional probabilities from present perils states
""")

def multiplanetary_given_present_perils():
    if present_perils_remainder() >= 0:
        return present_perils_remainder()
    return .0

def present_perils_remainder():
    return 1 - sum([st.session_state[transition] for transition in specifiable_transitions_from_present_perils])

specifiable_transitions_from_present_perils = [
    'Extinction given present perils',
    'Preequilibrium given present perils',
    'Preindustrial given present perils',
    'Industrial given present perils',
    'Future perils given present perils',
    'Interstellar given present perils'
]

for transition in specifiable_transitions_from_present_perils:
    if transition not in st.session_state:
        st.session_state[transition] = 0.1

if 'present_perils_remainder' not in st.session_state:
    st.session_state.present_perils_remainder = present_perils_remainder()

def update_transitions_given_present_perils_from_slider(transition_name):
    other_transitions = [transition for transition in specifiable_transitions_from_present_perils if transition != transition_name]
    st.session_state[transition_name] = st.session_state[transition_name + '_slider_value']
    # Reduce the values of the other transitions as much as need be to ensure that the sum of all transitions is 1
    excess_probability = -present_perils_remainder()
    for transition in reversed(other_transitions):
        if excess_probability > 0 and excess_probability <= st.session_state[transition]:
            # The difference is low enough to be absorbed by this transition, so we're done adjusting sliders
            st.session_state[transition] += present_perils_remainder()
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= st.session_state[transition]
            st.session_state[transition] = .0
        # If excess_probability is negative or 0, it will be added to the multiplanetary transition probability

def make_on_change_present_perils_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions_given_present_perils_from_slider(transition_name)
    return callback

for transition in specifiable_transitions_from_present_perils:
    st.slider(
    label=transition,
    min_value=0.0,
    max_value=1.0,
    value=st.session_state[transition],
    step=0.001,
    format="%f",
    on_change=make_on_change_present_perils_callback(transition),
    key=transition + '_slider_value')

st.slider(
    label='Multiplanetary given present perils',
    min_value=0.0,
    max_value=1.0,
    value=multiplanetary_given_present_perils(),
    disabled=True, format="%f")




# Section 5 - Transitional probabilities from future perils states

'---'

st.markdown("""## Transitional probabilities from future perils states
""")

def multiplanetary_given_future_perils():
    if future_perils_remainder() >= 0:
        return future_perils_remainder()
    return .0

def future_perils_remainder():
    return 1 - sum([st.session_state[transition] for transition in specifiable_transitions_from_future_perils])

specifiable_transitions_from_future_perils = [
    'Extinction given future perils',
    'Preequilibrium given future perils',
    'Preindustrial given future perils',
    'Industrial given future perils',
    'Interstellar given future perils'
]

for transition in specifiable_transitions_from_future_perils:
    if transition not in st.session_state:
        st.session_state[transition] = 0.1

if 'future_perils_remainder' not in st.session_state:
    st.session_state.future_perils_remainder = future_perils_remainder()

def update_transitions_given_future_perils_from_slider(transition_name):
    other_transitions = [transition for transition in specifiable_transitions_from_future_perils if transition != transition_name]
    st.session_state[transition_name] = st.session_state[transition_name + '_slider_value']
    # Reduce the values of the other transitions as much as need be to ensure that the sum of all transitions is 1
    excess_probability = -future_perils_remainder()
    for transition in reversed(other_transitions):
        if excess_probability > 0 and excess_probability <= st.session_state[transition]:
            # The difference is low enough to be absorbed by this transition, so we're done adjusting sliders
            st.session_state[transition] += future_perils_remainder()
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= st.session_state[transition]
            st.session_state[transition] = .0
        # If excess_probability is negative or 0, it will be added to the multiplanetary transition probability

def make_on_change_future_perils_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions_given_future_perils_from_slider(transition_name)
    return callback

for transition in specifiable_transitions_from_future_perils:
    st.slider(
    label=transition,
    min_value=0.0,
    max_value=1.0,
    value=st.session_state[transition],
    step=0.001,
    format="%f",
    on_change=make_on_change_future_perils_callback(transition),
    key=transition + '_slider_value')

st.slider(
    label='Multiplanetary given future perils',
    min_value=0.0,
    max_value=1.0,
    value=multiplanetary_given_future_perils(),
    disabled=True, format="%f")




# Section 6 Transitional probabilities from multiplanetary states

'---'

st.markdown("""## Transitional probabilities from multiplanetary states
""")

def interstellar_given_multiplanetary():
    if multiplanetary_remainder() >= 0:
        return multiplanetary_remainder()
    return .0

def multiplanetary_remainder():
    return 1 - sum([st.session_state[transition] for transition in specifiable_transitions_from_multiplanetary])

specifiable_transitions_from_multiplanetary = [
    'Extinction given multiplanetary',
    'Preequilibrium given multiplanetary',
    'Preindustrial given multiplanetary',
    'Industrial given multiplanetary',
    'Future perils given multiplanetary',
]

for transition in specifiable_transitions_from_multiplanetary:
    if transition not in st.session_state:
        st.session_state[transition] = 0.1

if 'multiplanetary_remainder' not in st.session_state:
    st.session_state.multiplanetary_remainder = multiplanetary_remainder()

def update_multiplanetary_transitions(transition_name):
    other_transitions = [transition for transition in specifiable_transitions_from_multiplanetary if transition != transition_name]
    st.session_state[transition_name] = st.session_state[transition_name + '_slider_value']
    # Reduce the values of the other transitions as much as need be to ensure that the sum of all transitions is 1
    excess_probability = -multiplanetary_remainder()
    for transition in reversed(other_transitions):
        if excess_probability > 0 and excess_probability <= st.session_state[transition]:
            # The difference is low enough to be absorbed by this transition, so we're done adjusting sliders
            st.session_state[transition] += multiplanetary_remainder()
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= st.session_state[transition]
            st.session_state[transition] = .0
        # If excess_probability is negative or 0, it will be added to the multiplanetary transition probability

def make_on_change_multiplanetary_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_multiplanetary_transitions(transition_name)
    return callback

for transition in specifiable_transitions_from_multiplanetary:
    st.slider(
    label=transition,
    min_value=0.0,
    max_value=1.0,
    value=st.session_state[transition],
    step=0.001,
    format="%f",
    on_change=make_on_change_multiplanetary_callback(transition),
    key=transition + '_slider_value')

st.slider(
    label='Interstellar given multiplanetary',
    min_value=0.0,
    max_value=1.0,
    value=interstellar_given_multiplanetary(),
    disabled=True, format="%f")

# st.write("""
#     On your assumptions...
#     The probability of becoming interstellar from a pre_equilibrium state = {{ calc.net_interstellar_from_pre_equilibrium() }}
#     The probability of becoming interstellar from a preindustrial state = {{ calc.net_interstellar_from_preindustrial() }}
#     The probability of becoming interstellar from an industrial state = {{ calc.net_interstellar_from_industrial() }}
#     The probability of becoming interstellar from a time of perils state = {{ calc.net_interstellar_from_perils() }}</p>
#     The probability of becoming interstellar from a multiplanetary state = {{ calc.net_interstellar_from_multiplanetary() }}</p>

#     *****

#     Therefore, if we consider eventual extinction and interstellar colonisation the only two outcomes...
#     a castatrophe that put us into a pre-equilibrium state would be {{ calc.pre_equilibrium_probability_reduction() }} as bad as an extinction event
#     a castatrophe that put us into a preindustrial state would be {{ calc.preindustrial_probability_reduction() }} as bad as an extinction event
#     a castatrophe that put us into an industrial state would be {{ calc.industrial_probability_reduction() }} as bad as an extinction event
#     and if we reached a multiplanetary state, it would increase our chance of becoming interstellar by {{ calc.multiplanetary_probability_increase() }}
# """)

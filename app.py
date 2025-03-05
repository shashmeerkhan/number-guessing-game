import streamlit as st
import random

# Initialize session state
if 'target' not in st.session_state or st.session_state.get('reset', False):
    st.session_state['target'] = random.randint(1, 100)
    st.session_state['attempts'] = 0
    st.session_state['guesses'] = []
    st.session_state['min_val'] = 1
    st.session_state['max_val'] = 100
    st.session_state['reset'] = False

st.title("Number Guessing Game")

# Custom Range in Sidebar
st.sidebar.header("Settings")
min_val = st.sidebar.number_input("Minimum Value", value=st.session_state['min_val'], step=1)
max_val = st.sidebar.number_input("Maximum Value", value=st.session_state['max_val'], step=1)

# Validate range and update game
if min_val >= max_val:
    st.sidebar.error("Minimum value must be less than Maximum value")
elif st.sidebar.button("Set Range"):
    st.session_state['min_val'] = min_val
    st.session_state['max_val'] = max_val
    st.session_state['target'] = random.randint(min_val, max_val)
    st.session_state['attempts'] = 0
    st.session_state['guesses'] = []
    st.session_state['reset'] = False
    st.success(f"New range set: {min_val} to {max_val}")

# Difficulty Levels with corresponding max attempts
difficulty_options = {
    "Easy": 10,
    "Medium": 7,
    "Hard": 5
}
difficulty = st.sidebar.selectbox("Select Difficulty", list(difficulty_options.keys()))
max_attempts = difficulty_options[difficulty]
st.sidebar.write(f"Max Attempts: {max_attempts}")

# User Guess Input
guess = st.number_input(
    "Enter your guess",
    min_value=st.session_state['min_val'],
    max_value=st.session_state['max_val'],
    step=1
)

# Game Logic
if st.button("Submit Guess"):
    if st.session_state['attempts'] < max_attempts:
        if guess not in st.session_state['guesses']:
            st.session_state['attempts'] += 1
            st.session_state['guesses'].append(guess)
            
            if guess == st.session_state['target']:
                st.success(f"Congratulations! You guessed {guess} correctly in {st.session_state['attempts']} attempts!")
                st.session_state['reset'] = True
            elif st.session_state['attempts'] >= max_attempts:
                st.error(f"Game Over! The number was {st.session_state['target']}")
                st.session_state['reset'] = True
            elif guess > st.session_state['target']:
                st.warning("Too High! Try again.")
            else:
                st.warning("Too Low! Try again.")
        else:
            st.warning("You've already guessed this number!")
    else:
        st.error(f"Game Over! The number was {st.session_state['target']}")

# Display game status
st.write(f"Attempts: {st.session_state['attempts']}/{max_attempts}")
st.write(f"Previous guesses: {', '.join(map(str, st.session_state['guesses']))}")

# Reset Button
if st.button("Reset Game"):
    st.session_state['target'] = random.randint(st.session_state['min_val'], st.session_state['max_val'])
    st.session_state['attempts'] = 0
    st.session_state['guesses'] = []
    st.session_state['reset'] = False
    st.rerun()

import streamlit as st
import random
import pandas as pd
import os
import time

from helpers.markdown import markdown_instructions


DATA = "data/example_data.csv"
RESULTS = "results/results.csv"
INDEX_COL = "id"
ADD_DRAW_BUTTON = True

if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.perf_counter()

# Load the sentences data
sentences = pd.read_csv(DATA, index_col=INDEX_COL)

def get_sample(sentences):
    selected_sentences = sentences.sample(2)
    st.session_state['sentence1'] = selected_sentences.iloc[0]
    st.session_state['sentence2'] = selected_sentences.iloc[1]
    st.session_state['index1'] = selected_sentences.index[0]
    st.session_state['index2'] = selected_sentences.index[1]

if "initialise" not in st.session_state:
    st.session_state["initialise"] = True
    if os.path.exists(RESULTS):
        os.remove(RESULTS)
    get_sample(sentences)
    
# Function to save the result
def save_result(winner, elapsed_time):

    winner_side = "None"
    if winner == "A":
        winner_side = "Left"
    elif winner == "B":
        winner_side = "Right"

    # Create a dataframe for the current result
    result_df = pd.DataFrame([{
        'A_id': st.session_state['index1'],
        'B_id': st.session_state['index2'],
        'winner_id': winner,
        'winner_side': winner_side,
        'elapsed_time': elapsed_time
    }])

    # Check if the results file exists, if not create it
    if os.path.exists(RESULTS):
        result_df.to_csv(RESULTS, mode='a', header=False, index=False)
    else:
        result_df.to_csv(RESULTS, index=False)

    # Refresh with a new pair of sentences
    get_sample(sentences)
    st.rerun()

def calculate_time(start,end):
    end_time = time.perf_counter()
    elapsed_time = end_time - st.session_state["start_time"]
    st.session_state["start_time"] = end_time  # Reset timer for next vote
    return f"{elapsed_time:.4f}"

# Set up the page
st.set_page_config(page_title="Voting Arena", page_icon="⚔️", layout="wide")

# Centered title with custom styling
st.markdown(
    markdown_instructions,
    unsafe_allow_html=True
)

# Display sentences side by side with some extra styling
colA, colB = st.columns(2)

with colA:
    st.write(f"<div class='column-title'>🅰️</div>", unsafe_allow_html=True)
    st.write(f"<div class='sentence-box'>{st.session_state['sentence1']['sentence']}</div>", unsafe_allow_html=True)

with colB:
    st.write(f"<div class='column-title'>🅱️</div>", unsafe_allow_html=True)
    st.write(f"<div class='sentence-box'>{st.session_state['sentence2']['sentence']}</div>", unsafe_allow_html=True)

# Voting button actions with custom styling

if ADD_DRAW_BUTTON:
    colA, col_Draw, colB = st.columns(3)
    with col_Draw:
        if st.button("Vote for a Draw", use_container_width=True, key='vote_draw', help="Click to vote for a draw"):
            time_elapsed = calculate_time(st.session_state["start_time"], time.perf_counter())
            save_result('Draw', time_elapsed)
            st.markdown("<div class='vote-message'>You voted for Sentence A!</div>", unsafe_allow_html=True)

with colA:
    if st.button("Vote for A", use_container_width=True, key='vote_a', help="Click to vote for Sentence A"):
        time_elapsed = calculate_time(st.session_state["start_time"], time.perf_counter())
        save_result('A', time_elapsed)
        st.markdown("<div class='vote-message'>You voted for Sentence A!</div>", unsafe_allow_html=True)

with colB:
    if st.button("Vote for B", use_container_width=True, key='vote_b', help="Click to vote for Sentence B"):
        time_elapsed = calculate_time(st.session_state["start_time"], time.perf_counter())
        save_result('B', time_elapsed)
        st.markdown("<div class='vote-message'>You voted for Sentence B!</div>", unsafe_allow_html=True)

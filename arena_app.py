import streamlit as st
import random
import pandas as pd
import os

from helpers.markdown import markdown_instructions


DATA = "data/example_data.csv"
RESULTS = "results/results.csv"
INDEX_COL = "id"
ADD_DRAW_BUTTON = True

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
def save_result(winner):
    # Create a dataframe for the current result
    result_df = pd.DataFrame([{
        'A_id': st.session_state['index1'],
        'B_id': st.session_state['index2'],
        'winner_id': winner,
    }])

    # Check if the results file exists, if not create it
    if os.path.exists(RESULTS):
        result_df.to_csv(RESULTS, mode='a', header=False, index=False)
    else:
        result_df.to_csv(RESULTS, index=False)

    # Refresh with a new pair of sentences
    get_sample(sentences)
    st.rerun()


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
            save_result('Draw')
            st.markdown("<div class='vote-message'>You voted for Sentence A!</div>", unsafe_allow_html=True)

with colA:
    if st.button("Vote for A", use_container_width=True, key='vote_a', help="Click to vote for Sentence A"):
        save_result('A')
        st.markdown("<div class='vote-message'>You voted for Sentence A!</div>", unsafe_allow_html=True)

with colB:
    if st.button("Vote for B", use_container_width=True, key='vote_b', help="Click to vote for Sentence B"):
        save_result('B')
        st.markdown("<div class='vote-message'>You voted for Sentence B!</div>", unsafe_allow_html=True)

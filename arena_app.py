import streamlit as st
import random
import pandas as pd
import os

from helpers.markdown import markdown_instructions

# Paths to the data and results files
DATA = "example_data.csv"
RESULTS = "results/results.csv"
INDEX_COL = "id"

# Load the sentences data
sentences = pd.read_csv(DATA, index_col=INDEX_COL)

if "initialise" not in st.session_state:
    st.session_state["initialise"] = True
    if os.path.exists(RESULTS):
        os.remove(RESULTS)

# Initialize session state for selected sentences if not already done
if 'sentence1' not in st.session_state or 'sentence2' not in st.session_state:
    selected_sentences = sentences.sample(2)
    st.session_state['sentence1'] = selected_sentences.iloc[0]
    st.session_state['sentence2'] = selected_sentences.iloc[1]
    st.session_state['index1'] = selected_sentences.index[0]
    st.session_state['index2'] = selected_sentences.index[1]

# Function to save the result
def save_result(winner_id, loser_id):
    # Create a dataframe for the current result
    result_df = pd.DataFrame([{
        'sentence1_id': st.session_state['sentence1']["sentence"],
        'sentence2_id': st.session_state['sentence2']["sentence"],
        'winner_id': winner_id,
        'loser_id': loser_id
    }])

    # Check if the results file exists, if not create it
    if os.path.exists(RESULTS):
        result_df.to_csv(RESULTS, mode='a', header=False, index=False)
    else:
        result_df.to_csv(RESULTS, index=False)

    # Refresh with a new pair of sentences
    new_sentences = sentences.sample(2).to_dict(orient='records')
    st.session_state['sentence1'] = new_sentences[0]
    st.session_state['sentence2'] = new_sentences[1]

import streamlit as st

# Set up the page
st.set_page_config(page_title="Voting Arena", page_icon="⚔️", layout="wide")

# Centered title with custom styling
st.markdown(
    markdown_instructions,
    unsafe_allow_html=True
)

# Display sentences side by side with some extra styling
col1, col2 = st.columns(2)

with col1:
    st.write(f"<div class='sentence-box'>{st.session_state['sentence1']['sentence']}</div>", unsafe_allow_html=True)

with col2:
    st.write(f"<div class='sentence-box'>{st.session_state['sentence2']['sentence']}</div>", unsafe_allow_html=True)

# Voting button actions with custom styling
with col1:
    if st.button("Vote for A", use_container_width=True, key='vote_a', help="Click to vote for Sentence A"):
        save_result(st.session_state['index1'], st.session_state['index2'])
        st.markdown("<div class='vote-message'>You voted for Sentence A!</div>", unsafe_allow_html=True)

with col2:
    if st.button("Vote for B", use_container_width=True, key='vote_b', help="Click to vote for Sentence B"):
        save_result(st.session_state['index2'], st.session_state['index1'])
        st.markdown("<div class='vote-message'>You voted for Sentence B!</div>", unsafe_allow_html=True)

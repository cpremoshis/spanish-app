import streamlit as st
import os
import pandas as pd

chat_topics_file = "./Chat Topics/Chat Topics.csv"
col_names = ['Week', 'Topics']

def open_topics_list():
    with open(chat_topics_file, 'r') as f:
        topics_df = pd.read_csv(f, names=col_names)

    return topics_df

topics_df = open_topics_list()

st.write(topics_df)
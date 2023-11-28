import streamlit as st
import os
import pandas as pd
import unicodedata


def open_topics_list():

    chat_topics_file = "./Chat Topics/Chat Topics.csv"
    col_names = ['Week', 'Topics']

    with open(chat_topics_file, 'r') as f:
        topics_df = pd.read_csv(f, names=col_names, encoding='utf-8')

    return topics_df

topics_df = open_topics_list()

#st.write(topics_df)

hardcode = 'Diplomacia Pública'
df_path = topics_df.iloc[4]['Week']

st.write("Hardcoded path bytes:", [hex(ord(c)) for c in hardcode])
st.write("DataFrame path bytes:", [hex(ord(c)) for c in df_path])
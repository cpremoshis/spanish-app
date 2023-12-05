import streamlit as st
import os
import pandas as pd
import unicodedata

def open_topics_list():
    with open('/mount/src/spanish-app/Topics.csv', 'r') as f:
        files_df = pd.read_csv(f, index_col=0, encoding='utf-8')

    topics_list = files_df['Topics'].tolist()

    return topics_list, files_df

topics_list, files_df = open_topics_list()

sentence_path = files_df[files_df['Topics'] == 'Economía']['Sentences'].iloc[0]
sentence_path = unicodedata.normalize('NFC', sentence_path)

hardcode = '/mount/src/spanish-app/Sentences/Economía/Economía.csv'
df_path = files_df[files_df['Topics'] == 'Sentences']['Sentences'].iloc[0]

col1, col2 = st.columns(2)
with col1:
    st.write("Hardcoded path bytes:", [hex(ord(c)) for c in hardcode])
with col2:
    st.write("DataFrame path bytes:", [hex(ord(c)) for c in sentence_path])




#sentence_path = '/mount/src/spanish-app/Sentences/Economía/Economía.csv'
#sentence_path = unicodedata.normalize('NFC', sentence_path)

#with open(sentence_path, 'r') as f:
#    test_df = pd.read_csv(f)

#st.write(test_df)
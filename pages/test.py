import streamlit as st
import os
import pandas as pd
import unicodedata


def open_sentences():
    sentences = "/mount/src/spanish-app/Sentences/Economía/Economía.csv"

    with open(sentences, 'r') as f:
        sentences_df = pd.read_csv(f, index_col=0)
    
    return sentences_df

senteces_df = open_sentences()

hardcode = './Sentences/Economía/audio/4_Economía_audio.mp3'
df_path = senteces_df.iloc[4]['Audio']

col1, col2 = st.columns(2)
with col1:
    st.write("Hardcoded path bytes:", [hex(ord(c)) for c in hardcode])
with col2:
    st.write("DataFrame path bytes:", [hex(ord(c)) for c in df_path])

#st.write(senteces_df[senteces_df['Week'] == 'USAID']['Topics'])

files = os.listdir("/mount/admin/install_path/")
st.write(files)
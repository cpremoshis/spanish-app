import streamlit as st
import os
import pandas as pd

file_path = "./Sentences/Política/Política.csv"

try:
    with open(file_path, 'r') as f:
        df = pd.read_csv(f, index_col=0)
    st.write(df)
except Exception as e:
    st.error(f"An error occurred: {e}")



hardcoded_path = './Sentences/Política/audio/0_Política_audio.mp3'
df_path = df.iloc[0]['Audio']

col1, col2 = st.columns(2):

col1:
    st.write("Hardcoded path bytes:", [hex(ord(c)) for c in hardcoded_path])
col2:
    st.write("DataFrame path bytes:", [hex(ord(c)) for c in df_path])


#st.audio('./Sentences/Política/audio/1_Política_audio.mp3')


#st.audio(audio_path)
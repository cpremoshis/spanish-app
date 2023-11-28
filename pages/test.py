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

st.audio('./Sentences/Política/audio/0_Política_audio.mp3')


#st.audio(audio_path)
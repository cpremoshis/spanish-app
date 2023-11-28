import streamlit as st
import os
import pandas as pd

file_path = "cpremoshis/spanish-app/Sentences/Economia/Economia.csv"

try:
    with open(file_path, 'r') as f:
        df = pd.read_csv(f, index_col=0)
    st.write(df)
except Exception as e:
    st.error(f"An error occurred: {e}")

audio = "./Sentences/Política/audio/48_Política_audio.mp3"

st.audio("./Sentences/Política/audio/48_Política_audio.mp3")
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

audio_path = df.iloc[0]['Audio']
audio_path = audio_path.encode('utf-8').decode('utf-8')

check = os.path.isfile(audio_path)
st.write(check)

st.audio(audio_path)
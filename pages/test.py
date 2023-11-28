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

import unicodedata

# Fetch the path from DataFrame
audio_path_df = df.iloc[0]['Audio']

# Normalize and re-encode
audio_path_df_normalized = unicodedata.normalize('NFKD', audio_path_df).encode('ascii', 'ignore').decode('ascii')

# Try using the normalized path
st.audio(audio_path_df_normalized)


hardcoded_path = './Sentences/Política/audio/0_Política_audio.mp3'
df_path = df.iloc[0]['Audio']

st.write("Hardcoded path bytes:", [hex(ord(c)) for c in hardcoded_path])
st.write("DataFrame path bytes:", [hex(ord(c)) for c in df_path])


#st.audio('./Sentences/Política/audio/1_Política_audio.mp3')


#st.audio(audio_path)
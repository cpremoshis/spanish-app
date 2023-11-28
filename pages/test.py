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

check = os.path.isfile(df.iloc[0]['Audio'])
st.write(check)

st.audio(df.iloc[0]['Audio'])
import streamlit as st
import os
import pandas as pd

file_path = "cpremoshis/spanish-app/Sentences/Economia/Economía.csv"


try:
    with open(file_path, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f, index_col=0)
    st.write(df)
except Exception as e:
    st.error(f"An error occurred: {e}")

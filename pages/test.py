import streamlit as st
import os
import pandas as pd

file = "cpremoshis/spanish-app/Sentences/Economía/Economía.csv"

with open('cpremoshis/spanish-app/Sentences/Economía/Economía.csv', 'r') as f:
    df = pd.read_csv(f, index_col=0)

st.write(df)
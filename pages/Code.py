import streamlit as st

#Page configuration
st.set_page_config(
    page_title="Code",
    page_icon="🇪🇸",
    initial_sidebar_state="collapsed",
    layout="wide"
    )

path = '/mount/src/spanish-app/app.py'

with open(path, 'r') as f:
    code = f.read()

st.code(code, line_numbers=True)
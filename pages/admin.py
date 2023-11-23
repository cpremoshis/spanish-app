import streamlit as st
import csv
from io import StringIO
import pandas as pd
import os

#Page configuration
st.set_page_config(
    page_title="Admin",
    )

def upload():
    tbd

tab1, tab2 = st.tabs(['Upload/Download Files', 'Feedback'])

with tab1:
    type_selection = st.selectbox("File type:", ['Vocab', 'Sentences'])
    action_selection = st.selectbox("Action:", ['Upload', 'Download'])

    if action_selection == 'Upload':
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            file_df = pd.read_csv(uploaded_file)
            st.write(file_df.head())
            #FINISH INSTRUCTIONS HERE

    if action_selection == "Download":
        dir_list = os.listdir("/mount/src/spanish-app")
        st.write(dir_list)

        #Show current working directory - /mount/src/spanish-app
        #cwd = os.getcwd()
        #st.write(cwd)

        #Show full directory for script location - /mount/src/spanish-app/pages
        #directory = os.path.dirname(os.path.abspath(__file__))
        #st.write(directory)
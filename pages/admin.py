import streamlit as st
import csv
from io import StringIO

#Page configuration
st.set_page_config(
    page_title="Admin",
    )

def upload():
    

tab1, tab2 = st.tabs(['Upload/Download Files', 'Feedback'])

with tab1:
    type_selection = st.selectbox("File type:", ['Vocab', 'Sentences'])
    action_selection = st.selectbox("Action:", ['Upload', 'Download'])

    if action_selection == 'Upload':
        uploaded_file = st.file_uploader("Choose a file")
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        string_data = stringio.read()
        st.write(string_data)


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
        
        if type_selection == "Vocab":
            vocab_files_path = "/mount/src/spanish-app/Vocab/"
            vocab_files_list = os.listdir(vocab_files_path)
            vocab_files_list.remove(".DS_Store")
            vocab_file_selected = st.selectbox("Select file:", vocab_files_list)
            vocab_file_to_download = vocab_files_path + vocab_file_selected

            with open(vocab_file_to_download, 'r') as f:
                download_button = st.download_button(
                    label = "Download file",
                    data = f,
                    file_name = vocab_file_selected,
                    mime = 'text/csv'
                    )
                
        if type_selection == "Sentences":
            sentences_files_path = "/mount/src/spanish-app/Sentences/"
            sentences_files_list = os.listdir(sentences_files_path)
            sentences_files_list.remove(".DS_Store")
            sentences_files_list.remove("Audio")
            sentence_file_selected = st.selectbox("Select file:", sentences_files_list)
            sentence_file_to_download = sentences_files_path + sentence_file_selected

            with open(sentence_file_to_download, 'r') as f:
                download_button = st.download_button(
                    label = "Download file",
                    data = f,
                    file_name = sentence_file_selected,
                    mime = 'text/csv'
                )
        
with tab2:
    feedback_file = "/mount/src/spanish-app/Feedback/reports.txt"

    with open(feedback_file, 'r') as f:
        reports = f.read().replace("\\n", "\n")
    
    st.write(reports)

    #Show files in specified directory
    dir_list = os.listdir("/mount/src/spanish-app/Feedback")
    st.write(dir_list)


#Show files in specified directory
#dir_list = os.listdir("/mount/src/spanish-app/Feedback")
#st.write(dir_list)

#Show current working directory - /mount/src/spanish-app
#cwd = os.getcwd()
#st.write(cwd)

#Show full directory for script - /mount/src/spanish-app/pages
#directory = os.path.dirname(os.path.abspath(__file__))
#st.write(directory)
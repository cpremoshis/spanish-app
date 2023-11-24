import streamlit as st
import csv
from io import StringIO
import pandas as pd
import os
from zipfile import ZipFile
import base64

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

        audio_files = os.listdir('/mount/src/spanish-app/Sentences/Audio/Week 9/')
        st.write(audio_files)


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
            sentences_csv_path = "/mount/src/spanish-app/Sentences/"
            sentences_csv_list = os.listdir(sentences_csv_path)
            sentences_csv_list.remove(".DS_Store")
            sentences_csv_list.remove("Audio")
            sentences_csv_list = [item.strip("_final.csv") for item in sentences_csv_list]
            week_selected = st.selectbox("Select file:", sentences_csv_list)
            sentence_csv_to_download = sentences_csv_path + week_selected + "_final.csv"

            download_csv_col, download_audio_col = st.columns(2)

            with download_csv_col:
                with open(sentence_csv_to_download, 'r') as f:
                    download_button = st.download_button(
                        label = "Download CSV",
                        data = f,
                        file_name = week_selected,
                        mime = 'text/csv'
                    )

            with download_audio_col:

                def zip_folder(folder_path, zip_filename):
                    if not os.path.exists(folder_path):
                        print(f"Error: Folder '{folder_path}' not found.")
                        return
                    
                    with ZipFile(zip_filename, 'w') as zip_file:
                        for foldername, subfolders, filenames in os.walk(folder_path):
                            for filename in filenames:
                                file_path = os.path.join(foldername, filename)
                                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

                    print(f"Zip file '{zip_filename}' created successfully.")

                folder_path = "/mount/src/spanish-app/Sentences/Audio/" + week_selected + "/"
                zip_filename = "/mount/src/spanish-app/Sentences/Audio/audio_files.zip"

                if st.button("Generate zip file"):
                    zip_folder(folder_path, zip_filename)

                if os.path.exists(zip_filename):
                    with open(zip_filename, 'rb') as f:
                        zip_contents = f.read()
                        b64 = base64.b64encode(zip_contents).decode()
                        href = f'<a href="data:file/zip;base64,{b64}" download="{week_selected + ".zip"}">Download zip</a>'
                        st.markdown(href, unsafe_allow_html=True)
        
with tab2:
    feedback_file = "/mount/src/spanish-app/Feedback/reports.txt"

    with open(feedback_file, 'r') as f:
        reports = f.read()
        download_button = st.download_button(
            label = "Download file",
            data = reports,
            file_name = "reports.txt",
            mime = 'text/plain'
        )

    st.write(reports)



#Show files in specified directory
#dir_list = os.listdir("/mount/src/spanish-app/Feedback")
#st.write(dir_list)

#Show current working directory - /mount/src/spanish-app
#cwd = os.getcwd()
#st.write(cwd)

#Show full directory for script - /mount/src/spanish-app/pages
#directory = os.path.dirname(os.path.abspath(__file__))
#st.write(directory)
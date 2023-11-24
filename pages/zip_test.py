import streamlit as st
import os
from zipfile import ZipFile
import base64

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

folder_path = "/mount/src/spanish-app/Sentences/Audio/"
zip_filename = "/mount/src/spanish-app/Sentences/Audio/audio_files.zip"

#Show files in specified directory
dir_list = os.listdir("/mount/src/spanish-app/Sentences/")
st.write(dir_list)

if st.button("Generate zip file"):
    zip_folder(folder_path, zip_filename)

if os.path.exists(zip_filename):
    with open(zip_filename, 'rb') as f:
        zip_contents = f.read()
        b64 = base64.b64encode(zip_contents).decode()
        href = f'<a href="data:file/zip;base64,{b64}" download="{zip_filename}">Download zip</a>'
        st.markdown(href, unsafe_allow_html=True)

#Show files in specified directory
#dir_list = os.listdir("/mount/src/spanish-app/Sentences/Audio/Week 9")
#st.write(dir_list)
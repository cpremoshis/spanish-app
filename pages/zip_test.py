import streamlit as st
import os
from zipfile import ZipFile

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
zip_filename = "audio_files.zip"

#Show files in specified directory
dir_list = os.listdir("/mount/src/spanish-app/")
st.write(dir_list)

if st.button("Generate zip file"):
    zip_folder(folder_path, zip_filename)

with open('/mount/src/spanish-app/audio_files.zip', 'rb') as f:
    download_button = st.button(
        label = "Download zip",
        file_name = zip_filename,
        mime = 'application/zip'
    )

#Show files in specified directory
#dir_list = os.listdir("/mount/src/spanish-app/Sentences/Audio/Week 9")
#st.write(dir_list)
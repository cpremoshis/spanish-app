import streamlit as st
import os
from zipfile import ZipFile
import base64

#Show files in specified directory
dir_list = os.listdir("/mount/src/spanish-app/")
st.write(dir_list)

def print_directory_contents(path):
    for root, dirs, files in os.walk(path):
        print(f"Current Directory: {root}")

        # Print subdirectories
        print("Subdirectories:")
        for directory in dirs:
            print(os.path.join(root, directory))

        # Print files
        print("Files:")
        for file in files:
            print(os.path.join(root, file))

        print("")

sentences_path = "/mount/src/spanish-app/Sentences/"
audio_path = "/mount/src/spanish-app/Audio/"

st.write(print_directory_contents(sentences_path))
st.write(print_directory_contents(audio_path))

#os.remove('/mount/src/spanish-app/Sentences/Audio/audio_files.zip')
import streamlit as st
import os
from zipfile import ZipFile
import base64

#Show files in specified directory
dir_list = os.listdir("/mount/src/spanish-app/")
st.write(dir_list)

#os.remove('/mount/src/spanish-app/Sentences/Audio/audio_files.zip')
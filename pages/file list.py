import streamlit as st
import os
import seedir as sd

#Show files in specified directory
sentences_path = '/mount/src/spanish-app/Sentences/'

sd.seedir(path=sentences_path, style='lines', itemlimit=10, depthlimit=2, exclude_folders='.git')

#os.remove('/mount/src/spanish-app/Sentences/Audio/audio_files.zip')
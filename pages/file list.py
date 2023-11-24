import streamlit as st
import os
from zipfile import ZipFile
import base64

#Show files in specified directory
dir_list = os.listdir("/mount/src/spanish-app/")
st.write(dir_list)

sentences_start_path = '/mount/src/spanish-app/Sentences/'

for root, dirs, files in os.walk(sentences_start_path):
	level = root.replace(sentences_start_path, '').count(os.sep)
	indent = ' ' * 4 * (level)
	st.write('{}{}/'.format(indent, os.path.basename(root)))

#os.remove('/mount/src/spanish-app/Sentences/Audio/audio_files.zip')
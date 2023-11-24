import streamlit as st
import os
from zipfile import ZipFile
import base64

os.remove('/mount/src/spanish-app/Sentences/Audio/audio_files.zip')
os.remove('/mount/src/spanish-app/audio_files.zip')
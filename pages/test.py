import streamlit as st
import os

def find_sentence_files():
    sentences_root_folder = "./Sentences"
    sentence_dir_list = os.listdir(sentences_root_folder)
    sentence_dir_list.remove(".DS_Store")
    sentence_files = {}

    for item in sentence_dir_list:
        folder_contents = os.listdir(sentences_root_folder + "/" + item)

        for file in folder_contents:
            if ".csv" in file:
                final_file = file
                sentence_files[file.strip('.csv')] = sentences_root_folder + "/" + item + "/" + final_file

    return sentence_files

sentence_files = find_sentence_files()
st.write(sentence_files)
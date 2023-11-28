import streamlit as st
import os
import pandas as pd
import unicodedata

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

def open_sentences(week):
 
    with open(sentence_files[week], 'r') as f:
        sentences_df = pd.read_csv(f, index_col=0, encoding='utf-8')
    
    return sentences_df



#st.write(topics_df)

hardcode = 'Diplomacia Pública'
df_path = topics_df.iloc[4]['Week']

st.write("Hardcoded path bytes:", [hex(ord(c)) for c in hardcode])
st.write("DataFrame path bytes:", [hex(ord(c)) for c in df_path])
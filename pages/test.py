import streamlit as st
import os
import pandas as pd

def find_vocab_files():
    vocab_dir_list = os.listdir("./Vocab")
    vocab_dir_list.remove(".DS_Store")
    vocab_files = {}

    for item in vocab_dir_list:
        key = item.replace('.csv', '')
        value = "./Vocab/" + key + ".csv"
        vocab_files[key] = value

    return vocab_files

vocab_files = find_vocab_files()

st.write(vocab_files)

for key in vocab_files.keys():
    st.write("ASCII values of key in vocab_files:", [ord(c) for c in key])

import streamlit as st
import csv
from io import StringIO
import pandas as pd
import os
from zipfile import ZipFile
import base64
import re
import openai
import configparser
from gtts import gTTS

#Page configuration
st.set_page_config(
    page_title="Admin",
    )


def upload():
    tbd

def generate_sentences(prompt):
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=[{'role':'system', 'content':'For each of the items in the provided list of Spanish words and phrases, generate a complete example sentence in Spanish along with its English translation. Each example sentence should contain at least one subject, a verb, and an object. Each row should contain only one Spanish-English sentence pair, with the Spanish and English separated by the "|" character. Do not include headers. Strictly follow this example for displaying the generated sentences: "El juicio por asesinato se llevará a cabo el próximo mes. | The murder trial will take place next month. \n La música tiene el poder de evocar emociones profundas. | Music has the power to evoke deep emotions."'},
                  {'role':'user', 'content':prompt}],
        temperature=0.1
    )

    generated_sentences = response.choices[0].message.content

    return generated_sentences

def process_sentence_chunks(vocab_list, chunk_size=20):
    for i in range(0, len(vocab_list), chunk_size):
        yield vocab_list[i:i + chunk_size]

def process_generated_sentences(input):
    final_sentences = []

    for item in input:
        lines = item.strip().split("\n")
        for item in lines:
            final_sentences.append(item)

    data = [line.strip().split(" | ") for line in final_sentences]
    df = pd.DataFrame(data, columns=['Spanish', 'English'])

    return df

def google_speech_sentences(row, df):
    text = row['Spanish']
    index_label = row.name
    index_number = df.index.get_loc(index_label)

    tts = gTTS(text=text, lang="es")

    audio_file_path = sentence_audio_path
    os.makedirs(audio_file_path, exist_ok=True)
    audio_file_path += str(index_number) + "_" + week_selection + "_" "audio.mp3"

    tts.save(audio_file_path)

    return audio_file_path

def create_sentences_from_vocab(vocab_df):
    try:
        re_pattern = r'\([^)]*\)'

        spanish_vocab = [item for item in vocab_df['Spanish']]
        spanish_vocab = [re.sub(re_pattern, '', word).strip() for word in spanish_vocab]

        all_sentences = []

        #Sends chunks of vocab to ChatGPT for sentence generation, adds results to list
        for chunk in process_sentence_chunks(spanish_vocab):
            generated_sentences = generate_sentences(str(chunk))
            all_sentences.append("\n" + generated_sentences)

        #Splitting generated sentences into properly formatted list in preparation for audio creation
        sentences_df = process_generated_sentences(all_sentences)

        #Audio generation and saving of DataFrame as CSV
        sentences_df.loc[:,'Audio'] = sentences_df.apply(google_speech_sentences, df=sentences_df, axis=1)
        sentences_df['Audio'] = sentences_df['Audio'].str.replace("/Users/casey/Documents/PythonProjects/Spanish Learning App", ".")
        sentences_df.to_csv(sentence_csv_path + week_selection + ".csv")

        status = 1

        return status
    
    except Exception as error:

        return error


#API key
try:
    #openai.api_key = st.secrets['openai']['api_key']
    config = configparser.ConfigParser()
    config.read('/Users/casey/Documents/PythonProjects/Spanish Learning App/config.ini')
    openai.api_key = config['openai']['api_key']
except:
    pass


try:
    tab1, tab2, tab3, tab4 = st.tabs(['Upload/Download Files', 'Generate content', 'Feedback', 'File list'])

    with tab1:
        with st.form("data_selection_form"):
            data_column1, data_column2, data_column3, data_column4 = st.columns(4)

            with data_column1:
                action_selection = st.selectbox("Action:", ['Upload', 'Download'])
            with data_column2:
                type_selection = st.selectbox("File type:", ['Vocab', 'Sentences'])
            with data_column3:
                week_selection = st.text_input("Week:")
                week_selection = "Week " + str(week_selection)
            with data_column4:
                st.markdown(" ")
                st.text("")
                submit_button = st.form_submit_button("Confirm selection")

        st.write("Selection: " + type_selection + " - " + action_selection + " - " + week_selection)

        #Needed inputs for processing of uploaded CSV
        df_columns = ['Spanish', 'English']
        sentence_csv_path = "/Users/casey/Documents/PythonProjects/Spanish Learning App/Sentences/" + week_selection + "/"
        sentence_audio_path = sentence_csv_path + "audio/"

        if action_selection == 'Upload':
            uploaded_file = st.file_uploader("Choose a file. Processing begins immediately upon upload.")
            if uploaded_file is not None:
                file_df = pd.read_csv(uploaded_file, names=df_columns)

                st.write("Preview:")
                st.write(file_df.head())

                processing_container = st.empty()
                processing_container.warning('Processing file. Please wait.')
                
                status = create_sentences_from_vocab(file_df)
                
                if status == 1:
                    processing_container.success("Processing success.")
                else:
                    processing_container.write(status)

        if action_selection == "Download":
            
            if type_selection == "Vocab":
                vocab_files_path = "//Users/casey/Documents/PythonProjects/Spanish Learning App/Vocab/"
                vocab_files_list = os.listdir(vocab_files_path)
                vocab_files_list.remove(".DS_Store")
                vocab_file_selected = st.selectbox("Select file:", vocab_files_list)
                vocab_file_to_download = vocab_files_path + vocab_file_selected

                with open(vocab_file_to_download, 'r') as f:
                    download_button = st.download_button(
                        label = "Download file",
                        data = f,
                        file_name = vocab_file_selected,
                        mime = 'text/csv'
                        )
                    
            if type_selection == "Sentences":
                sentences_csv_path = "/Users/casey/Documents/PythonProjects/Spanish Learning App/Sentences/" + week_selection + "/"
                sentences_csv_list = os.listdir(sentences_csv_path)
                sentences_csv_list.remove(".DS_Store")
                sentences_csv_list.remove("audio")
                week_selection = st.selectbox("Select file:", sentences_csv_list)
                sentence_csv_to_download = sentences_csv_path + week_selection

                download_csv_col, download_audio_col = st.columns(2)

                with download_csv_col:
                    with open(sentence_csv_to_download, 'r') as f:
                        download_button = st.download_button(
                            label = "Download CSV",
                            data = f,
                            file_name = week_selection,
                            mime = 'text/csv'
                        )

                with download_audio_col:

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

                    folder_path = "/Users/casey/Documents/PythonProjects/Spanish Learning App/Sentences/" + week_selection + "/audio/"
                    zip_filename = "/Users/casey/Documents/PythonProjects/Spanish Learning App/Sentences/" + week_selection + "/" + "audio_files.zip"

                    if st.button("Generate zip file"):
                        zip_folder(folder_path, zip_filename)

                    if os.path.exists(zip_filename):
                        with open(zip_filename, 'rb') as f:
                            zip_contents = f.read()
                            b64 = base64.b64encode(zip_contents).decode()
                            href = f'<a href="data:file/zip;base64,{b64}" download="{week_selection + ".zip"}">Download zip</a>'
                            st.markdown(href, unsafe_allow_html=True)
            
    with tab2:
        st.error("Under construction.")

    with tab3:
        
        try:
            feedback_file = "/Users/casey/Documents/PythonProjects/Spanish Learning App/Feedback/reports.txt"

            with open(feedback_file, 'r') as f:
                reports = f.read()
                download_button = st.download_button(
                    label = "Download report",
                    data = reports,
                    file_name = "reports.txt",
                    mime = 'text/plain'
                )

            st.write(reports)

        except:
            st.error("No file found.")

    with tab4:
        st.error("Under construction.")
except:
    st.error("Access denied.")


#Show files in specified directory
#dir_list = os.listdir("/mount/src/spanish-app/Feedback")
#st.write(dir_list)

#Show current working directory - /mount/src/spanish-app
#cwd = os.getcwd()
#st.write(cwd)

#Show full directory for script - /mount/src/spanish-app/pages
#directory = os.path.dirname(os.path.abspath(__file__))
#st.write(directory)
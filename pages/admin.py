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
        sentences_df['Audio'] = sentences_df['Audio'].str.replace("/mount/src/spanish-app", ".")
        sentences_df.to_csv(sentence_csv_path + week_selection + ".csv")

        status = 1

        return status
    
    except Exception as error:

        return error


#API key
#try:
    #openai.api_key = st.secrets['openai']['api_key']
    #config = configparser.ConfigParser()
    #config.read('/Users/casey/Documents/PythonProjects/Spanish Learning App/config.ini')
    #openai.api_key = config['openai']['api_key']
#except:
#    pass


try:
    tab1, tab2, tab3, tab4 = st.tabs(['Upload/Download Files', 'Generate content', 'Feedback', 'File list'])

    with tab1:
        st.error("Access denied.")
            
    with tab2:
        st.error("Access denied.")

    with tab3:
        
        try:
            feedback_file = "/mount/src/spanish-app/Feedback/reports.txt"

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
        st.error("Access denied.")
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
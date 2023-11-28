import streamlit as st
from gtts import gTTS
from io import BytesIO
#import speech_recognition as sr
#from audio_recorder_streamlit import audio_recorder
import csv
import openai
import os.path
import re
import pandas as pd
import random
from datetime import datetime
import configparser
import unicodedata

#Page configuration
st.set_page_config(
    page_title="Adelante y Más Allá",
    page_icon="🇪🇸",
    initial_sidebar_state="collapsed"
    )

#API key
openai.api_key = st.secrets['openai']['api_key']
#config = configparser.ConfigParser()
#config.read('config.ini')
#openai.api_key = config['openai']['api_key']

@st.cache_data()
def open_vocab_list(week):

    vocab_file_path = vocab_files[week]

    with open(vocab_file_path, 'r') as f:
        vocab_reader = csv.reader(f)

        vocab_dict = {}

        for row in vocab_reader:
            if row:
                key = row[0]
                value = row[1]
                vocab_dict[key] = value
            else:
                pass

    return vocab_dict

@st.cache_data
def open_sentence_list(week_selection):

    sentence_file_path = sentence_files[week_selection]

    with open(sentence_file_path, 'r') as f:
        sentence_reader = csv.reader(f)

        sentence_dict = {}

        for row in sentence_reader:
            if row:
                key = row[0]
                value = row[1]
                sentence_dict[key] = value
            else:
                pass

    return sentence_dict

@st.cache_data
def open_topics_list():

    chat_topics_file = "./Chat Topics/Chat Topics.csv"
    col_names = ['Week', 'Topics']

    with open(chat_topics_file, 'r') as f:
        topics_df = pd.read_csv(f, names=col_names, encoding='utf-8')

    def normalize_characters(text):
        return unicodedata.normalize('NFC', text)
    
    topics_df['Week'] = topics_df['Week'].apply(normalize_characters)

    return topics_df

def google_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

def google_speech_sentences(row, df):
    text = row['Spanish']
    index_label = row.name
    index_number = df.index.get_loc(index_label)

    tts = gTTS(text=text, lang="es")

    audio_file_path = sentence_audio_path + st.session_state['week_selection'] + "/" + "audio/"
    os.makedirs(audio_file_path, exist_ok=True)
    audio_file_path += str(index_number) + "_" + st.session_state['week_selection'] + "_" "audio.mp3"

    tts.save(audio_file_path)

    return audio_file_path

def recognize_speech_from_audio(audio_data, lang_code):
    recognizer = sr.Recognizer()
    with sr.AudioFile(BytesIO(audio_data)) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language=lang_code)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Error; request failed"

def vocab_review():
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

def chat_with_gpt(topics, prompt):
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=[{'role':'user', 'content':prompt},
                  {'role':'system', 'content':f"You are a teacher having a discussion with your student. Only speak in Spanish. Ensure your responses are always 150 tokens or less. Offer your students a mix of questions and opinions, do not just ask questions. Do not restart the conversation from the beginning. Focus on these topics one at a time but allow for mild deviation: {topics}."}],
        max_tokens=150,
        temperature=0.8
    )

    response_text = response.choices[0].message.content

    return response_text

def write_chat_history():
    st.write(st.session_state['history'])

def process_generated_sentences(input):
    final_sentences = []

    for item in input:
        lines = item.strip().split("\n")
        for item in lines:
            final_sentences.append(item)

    data = [line.strip().split(" | ") for line in final_sentences]
    df = pd.DataFrame(data, columns=['Spanish', 'English'])

    return df

def main():

    #Page layout
    st.title("Adelante y Más Allá")

    #Adds default 'week_selection' to session state
    if "week_selection" not in st.session_state:
        st.session_state['week_selection'] = "Week 9"

    #Creates list of only Spanish phrases from the vocab dict
    #spanish_vocab = [re.sub(re_pattern, '', word).strip() for word in word_pairs.keys()]

    column1, column2 = st.columns(2)

    with column1:
        tool_type = st.selectbox("Select tool:",
        ["Vocab review", "Sentences", "Conversation"],
        )
    with column2:
        weeks_list = sentence_files.keys()
        st.session_state['week_selection'] = st.selectbox("Select week:", weeks_list)

    if tool_type == "Vocab review":

        # Dictionary of Spanish-English word pairs
        word_pairs = open_vocab_list(st.session_state['week_selection'])

        try:
            if 'current_vocab_position' not in st.session_state:
                st.session_state.current_vocab_position = 0

            if 'vocab_review_order' not in st.session_state:
                st.session_state.vocab_review_order = random.sample(range(0, len(word_pairs)), len(word_pairs))

            def vocab_previous_click():
                if st.session_state.current_vocab_position <= 0:
                    st.session_state.current_vocab_position = len(st.session_state.vocab_review_order) - 1
                else:
                    st.session_state.current_vocab_position -= 1
            def vocab_next_click():
                if st.session_state.current_vocab_position >= len(st.session_state.vocab_review_order) - 1:
                    st.session_state.current_vocab_position = 0
                else:
                    st.session_state.current_vocab_position += 1

            with st.container():

                col_left, col_right = st.columns(2)
                col_left.button("Previous", use_container_width=True, on_click=vocab_previous_click)
                col_right.button("Next", use_container_width=True, on_click=vocab_next_click)

                #st.write(st.session_state.current_vocab_position)
                #st.write(st.session_state.vocab_review_order)
                vocab_link_number = st.session_state.vocab_review_order[st.session_state.current_vocab_position]
                #st.write(vocab_link_number)

                #st.audio(sentences_df.iloc[vocab_link_number]['Audio'])

                st.subheader("🇪🇸 " + list(word_pairs)[vocab_link_number], divider='orange')
                st.text("  \n")
                st.subheader("🇺🇸 " + list(word_pairs.values())[vocab_link_number], divider='orange')

            #Print debugging information
            #st.write(f"Word pairs: {word_pairs}")

        except Exception as error:
            container = st.empty()
            container.write(error)

    if tool_type == "Sentences":
        # https://docs.streamlit.io/library/advanced-features/button-behavior-and-examples

        if 'current_position' not in st.session_state:
            st.session_state.current_position = 0

        container = st.container()

        @st.cache_data
        def open_sentences(week):
            sentences_df = None
            check_for_sentences = os.path.isfile(sentence_files[str(week)])

            if check_for_sentences == True:
                with open(sentence_files[week], 'r') as f:
                    sentences_df = pd.read_csv(f, index_col=0, encoding='utf-8')
            
            return sentences_df
        
        try:
            sentences_df = open_sentences(st.session_state['week_selection'])

            if 'review_order' not in st.session_state:
                st.session_state.review_order = random.sample(range(0, len(sentences_df)), len(sentences_df))

            def previous_click():
                if st.session_state.current_position <= 0:
                    st.session_state.current_position = len(st.session_state.review_order) - 1
                else:
                    st.session_state.current_position -= 1
            def next_click():
                if st.session_state.current_position >= len(st.session_state.review_order) - 1:
                    st.session_state.current_position = 0
                else:
                    st.session_state.current_position += 1

            with st.container():

                col_left, col_right = st.columns(2)
                col_left.button("Previous", use_container_width=True, on_click=previous_click)
                col_right.button("Next", use_container_width=True, on_click=next_click)

                #st.write(st.session_state.current_position)
                #st.write(st.session_state.review_order)
                link_number = st.session_state.review_order[st.session_state.current_position]
                #st.write(link_number)

                audio_path = sentences_df.iloc[link_number]['Audio']
                normalized_audio_path = unicodedata.normalize('NFC', audio_path)
                st.audio(normalized_audio_path)

                st.subheader("🇪🇸 " + sentences_df.iloc[link_number]['Spanish'], divider='orange')
                #st.write(sentences_df.iloc[link_number]['Spanish'])
                st.text("  \n")
                st.subheader("🇺🇸 " + sentences_df.iloc[link_number]['English'], divider='orange')
                #st.write(sentences_df.iloc[link_number]['English'])

                def submit_report():
                    now = datetime.now()
                    message = str(now) + "\n" + str(link_number) + "\n" + str(sentences_df.iloc[link_number]['Spanish'] + "\n" + str(sentences_df.iloc[link_number]['English']))
                    with open("./Feedback/reports.txt", 'a') as f:
                        f.write("\n" + message + "\n")
                    st.toast("✅ Report submitted!")

                col_left2, col_right2 = st.columns(2)
                st.write("  \n")
                col_left2.caption("All sentences are generated by AI.  \nPlease flag any issues for review.")
                col_left2.button("Flag for review 🚩", on_click=submit_report)

        except Exception as error:
            container = st.empty()
            container.write(error)

    if tool_type == "Conversation":

        st.subheader("Chat with GPT", divider='orange')
        st.write("Begin by hitting 'Submit' for the pre-written message.")

        text_box = st.text_area('Type here:', "Hablemos de un tema de su elección.")
        submit_button = st.button("Submit")

        topics_df = open_topics_list()

        try:
            
            
            if 'history' not in st.session_state:
                st.session_state['history'] = ""

            if 'conversation_history' not in st.session_state:
                st.session_state['conversation_history'] = []

            if submit_button:
                # Store user input in the session state immediately after the button is pressed
                st.session_state['user_input'] = text_box
                st.session_state['conversation_history'].append(f"User: {st.session_state['user_input']}")

                gpt_response = chat_with_gpt(topics_df[st.session_state['week_selection']], "\n\n".join(st.session_state['conversation_history']))
                st.session_state['conversation_history'].append(f"GPT: {gpt_response}")

                # Update the history
                st.session_state['history'] += f"  \nUser: {st.session_state['user_input']}  \nGPT: {gpt_response}  \n"

            # Display the chat history outside the if block
            write_chat_history()
        except Exception as error:
            st.write(error)

#Dictionaries of vocab and sentence files
#Update each time new week is added
#root_file_path = "/Users/casey/Documents/PythonProjects/Spanish Learning App/"

#Show files in specified directory
@st.cache_data()
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


#vocab_files = {
#    "Week 9": "./Vocab/Week 9.csv",
#    "Week 10": "./Vocab/Week 10.csv",
#    "Week 11": "./Vocab/Week 11.csv",
#    "Administración y Gerencia": "./Vocab/Administración y Gerencia.csv",
#    "Consular": "./Vocab/Consular.csv",
#    "Diplomacia Pública": "./Vocab/Diplomacia Pública.csv",
#    "Economía": "./Vocab/Economía.csv",
#    "Política": "./Vocab/Política.csv",
#    "Seguridad": "./Vocab/Seguridad.csv",
#    "USAID": "./Vocab/USAID.csv",
#    "Vocabulario General": "./Vocab/Vocabulario General.csv"
#    }

@st.cache_data()
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

#sentence_files = {
#    "Week 9": "./Sentences/Week 9/Week 9.csv",
#    "Week 10": "./Sentences/Week 10/Week 10.csv",
#    "Week 11": "./Sentences/Week 11/Week 11.csv",
#    "Administración y Gerencia": "./Sentences/Administración y Gerencia/Administración y Gerencia.csv",
#    "Consular": "./Sentences/Consular/Consular.csv",
#    "Diplomacia Pública": "./Sentences/Diplomacia Pública/iplomacia Pública.csv",
#    "Economía": "./Sentences/Economía/Economía.csv",
#    "Política": "./Sentences/Política/Política.csv",
#    "Seguridad": "./Sentences/Seguridad/Seguridad.csv",
#    "USAID": "./Sentences/USAID/USAID.csv",
#    "Vocabulario General": "./Sentences/Vocabulario General/Vocabulario General.csv"
#}



#Sets default 'word_index'
if 'word_index' not in st.session_state:
    st.session_state.word_index = 0

#Regular expression to remove vocab items with parentheses
re_pattern = r'\([^)]*\)'

#Path to sentence audio files
sentence_audio_path = "./Sentences/"

if __name__ == "__main__":
    main()
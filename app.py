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
#import configparser
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
def open_topics_list():
    with open('./Topics.csv', 'r') as f:
        files_df = pd.read_csv(f, index_col=0, encoding='utf-8')

    topics_list = files_df['Topics'].tolist()

    return topics_list, files_df

@st.cache_data()
def open_vocab_list(week, files_df):

    vocab_file_path = files_df[files_df['Topics'] == week]['Vocab'].iloc[0]
    vocab_file_path = unicodedata.normalize('NFC', vocab_file_path)

    with open(vocab_file_path, 'r') as f:
        df = pd.read_csv(f, index_col=0, encoding='utf-8')

    vocab_dict = {}

    for index, row in df.iterrows():
        vocab_dict[row['Spanish']] = row['English']

    return vocab_dict

@st.cache_data
def open_chat_topics_list():

    chat_topics_file = "./Chat Topics/Chat Topics.csv"
    col_names = ['Week', 'Topics']

    with open(chat_topics_file, 'r') as f:
        topics_df = pd.read_csv(f, names=col_names, encoding='utf-8')

    #def normalize_characters(text):
    #    return unicodedata.normalize('NFC', text)
    
    #topics_df['Week'] = topics_df['Week'].apply(normalize_characters)

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

    if 'spanish_display_status' not in st.session_state:
        st.session_state['spanish_display_status'] = True

    if 'english_display_status' not in st.session_state:
        st.session_state['english_display_status'] = True

    def toggle_spanish_display():
        if st.session_state['spanish_display_status'] == True:
            st.session_state['spanish_display_status'] = False
        else:
            st.session_state['spanish_display_status'] = True

    def toggle_english_display():
        if st.session_state['english_display_status'] == True:
            st.session_state['english_display_status'] = False
        else:
            st.session_state['english_display_status'] = True

    topics_list, files_df = open_topics_list()

    column1, column2 = st.columns(2)

    with column1:
        tool_type = st.selectbox("Select tool:",
        ["Vocab review", "Sentences", "Conversation"],
        )
    with column2:
        st.session_state['week_selection'] = st.selectbox("Select topic:", topics_list)

    if tool_type == "Vocab review":
        #st.error("Consider adding audio function")
        
        # Dictionary of Spanish-English word pairs
        word_pairs = open_vocab_list(st.session_state['week_selection'], files_df)

        try:
            if 'current_vocab_position' not in st.session_state:
                st.session_state.current_vocab_position = 0
            elif st.session_state.current_vocab_position > len(word_pairs):
                st.session_state.current_vocab_position = 0

            if 'vocab_review_order' not in st.session_state:
                st.session_state.vocab_review_order = random.sample(range(0, len(word_pairs)), len(word_pairs))
            elif len(st.session_state.vocab_review_order) > len(word_pairs):
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
                
                vocab_link_number = st.session_state.vocab_review_order[st.session_state.current_vocab_position]
                
                #st.write(len(word_pairs))
                #st.write(st.session_state.current_vocab_position)
                #st.write(st.session_state.vocab_review_order)
                #st.write(vocab_link_number)
                #st.audio(sentences_df.iloc[vocab_link_number]['Audio'])

                vocab_display_left, vocab_display_right = st.columns(2)
                vocab_display_left.button("Toggle English 🇺🇸", key='english vocab toggle', type="primary", use_container_width=True, on_click=toggle_english_display)
                vocab_display_right.button("Toggle Spanish 🇪🇸", key='spanish vocab toggle', type="primary", use_container_width=True, on_click=toggle_spanish_display)

                vocab_display = st.container()

                if st.session_state['spanish_display_status'] == True:
                    vocab_display.subheader("🇪🇸 " + list(word_pairs)[vocab_link_number], divider='orange')
                    vocab_display.text("  \n")
                if st.session_state['english_display_status'] == True:
                    vocab_display.subheader("🇺🇸 " + list(word_pairs.values())[vocab_link_number], divider='orange')

            #Print debugging information
            #st.write(f"Word pairs: {word_pairs}")

        except Exception as error:
            container = st.empty()
            container.write(error)

    if tool_type == "Sentences":
        # https://docs.streamlit.io/library/advanced-features/button-behavior-and-examples

        container = st.container()

        @st.cache_data
        def open_sentences(week):
            sentences_df = None

            sentence_path = files_df[files_df['Topics'] == week]['Sentences'].iloc[0]
            sentence_path = unicodedata.normalize('NFC', sentence_path)

            with open(sentence_path, 'r') as f:
                sentences_df = pd.read_csv(f, index_col=0, encoding='utf-8')
        
            return sentences_df
        
        try:
            sentences_df = open_sentences(st.session_state['week_selection'])

            if 'current_position' not in st.session_state:
                st.session_state.current_position = 0
            elif st.session_state.current_position > len(sentences_df):
                st.session_state.current_position = 0

            if 'review_order' not in st.session_state:
                st.session_state.review_order = random.sample(range(0, len(sentences_df)), len(sentences_df))
            elif len(st.session_state.review_order) > len(sentences_df):
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

                sentence_display_left, sentence_display_right = st.columns(2)
                sentence_display_left.button("Show/hide English", key='english sentences toggle', type="primary", use_container_width=True, on_click=toggle_english_display)
                sentence_display_right.button("Show/hide Spanish", key='spanish sentences toggle', type="primary", use_container_width=True, on_click=toggle_spanish_display)

                sentence_display = st.container()

                def submit_report():
                    now = datetime.now()
                    message = str(now) + "\n" + str(link_number) + "\n" + str(sentences_df.iloc[link_number]['Spanish'] + "\n" + str(sentences_df.iloc[link_number]['English']))
                    with open("./Feedback/reports.txt", 'a') as f:
                        f.write("\n" + message + "\n")
                    st.toast("✅ Report submitted!")

                col_left2, col_right2 = st.columns(2)
                st.write("  \n")

                with col_left2:

                    if st.session_state['spanish_display_status'] == True:
                        sentence_display.subheader("🇪🇸 " + sentences_df.iloc[link_number]['Spanish'], divider='orange')
                        sentence_display.text("  \n")
                    if st.session_state['english_display_status'] == True:
                        sentence_display.subheader("🇺🇸 " + sentences_df.iloc[link_number]['English'], divider='orange')
                 
                    col_left2.write("  \n  ")
                    col_left2.write("  \n  ")
                    col_left2.write("  \n  ")
                    col_left2.write("  \n  ")

                    col_left2.button("Flag for review 🚩", on_click=submit_report)
                    col_left2.caption("All sentences are generated by AI.  \nPlease flag any issues for review.")

        except Exception as error:
            container = st.empty()
            container.write(error)

    if tool_type == "Conversation":

        incomplete_topics = ['Common Verbs 1 - 100', 'Common Verbs 101 - 200', 'Common Verbs 201 - 300', 'Common Verbs 301 - 400', 'Common Verbs 401 - 503', 'Frases con Tener']
        if st.session_state['week_selection'] in incomplete_topics:
            st.error("Chat with GPT has not yet been configured to work with the topic that you've selected. Please make another selection.")
        
        st.subheader("Chat with GPT", divider='orange')
        st.write("Begin by hitting 'Submit' for the pre-written message.")

        text_box = st.text_area('Type here:', "Hablemos de un tema de su elección.")
        submit_button = st.button("Submit")

        try:
            chat_topics_df = open_chat_topics_list()
            
            if 'history' not in st.session_state:
                st.session_state['history'] = ""

            if 'conversation_history' not in st.session_state:
                st.session_state['conversation_history'] = []

            topics = chat_topics_df[chat_topics_df['Week'] == st.session_state['week_selection']]['Topics'].iloc[0]

            if submit_button:
                # Store user input in the session state immediately after the button is pressed
                st.session_state['user_input'] = text_box
                st.session_state['conversation_history'].append(f"User: {st.session_state['user_input']}")

                gpt_response = chat_with_gpt(topics, "\n\n".join(st.session_state['conversation_history']))
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

#Sets default 'word_index'
if 'word_index' not in st.session_state:
    st.session_state.word_index = 0

#Regular expression to remove vocab items with parentheses
re_pattern = r'\([^)]*\)'

#Path to sentence audio files
sentence_audio_path = "./Sentences/"

if __name__ == "__main__":
    main()

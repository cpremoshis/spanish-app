import streamlit as st
from gtts import gTTS
from io import BytesIO
#import speech_recognition as sr
#from audio_recorder_streamlit import audio_recorder
import csv
import configparser
import openai
import os.path
import re
import pandas as pd
import random
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

#Page configuration
st.set_page_config(
    page_title="Adelante y Más Allá",
    page_icon="🇪🇸"
    )

#API key
openai.api_key = st.secrets['openai']['api_key']

@st.cache_data
def open_vocab_list(week_selection):

    vocab_file_path = vocab_files[week_selection]

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

    audio_file_path = sentence_audio_path + st.session_state['week_selection'] + "/"
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

def chat_with_gpt(prompt):
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=[{'role':'user', 'content':prompt},
                  {'role':'system', 'content':"You are a teacher having a discussion with your student. Only speak in Spanish. Ensure your responses are always 150 tokens or less. Offer your students a mix of questions and opinions, do not just ask questions. Do not restart the conversation from the beginning. Focus on these topics one at a time but allow for mild deviation: issues facing refugees, personal online security."}],
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

    column1, column2 = st.columns(2)

    with column1:
        tool_type = st.selectbox("Select tool:",
        ["Vocab review", "Sentences", "Conversation"],
        )
    with column2:
        week_selection = st.selectbox("Select week:",
        ['Week 9']
        )

    if tool_type == "Vocab review":
        st.error("Add audio function")
        
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

            st.subheader("Spanish", divider='orange')
            st.write(list(word_pairs)[vocab_link_number])

            st.subheader("English", divider='orange')
            st.write(list(word_pairs.values())[vocab_link_number])

        #Print debugging information
        #st.write(f"Word pairs: {word_pairs}")

    if tool_type == "Sentences":
        # https://docs.streamlit.io/library/advanced-features/button-behavior-and-examples

        if 'current_position' not in st.session_state:
            st.session_state.current_position = 0

        container = st.container()

        @st.cache_data
        def open_sentences():
            check_for_sentences = os.path.isfile(sentence_files[week_selection])

            if check_for_sentences == True:
                with open(sentence_files[week_selection], 'r') as f:
                    sentences_df = pd.read_csv(f, index_col=0)
            
            return sentences_df
        
        try:
            sentences_df = open_sentences()

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

                st.audio(sentences_df.iloc[link_number]['Audio'])

                st.subheader("Spanish", divider='orange')
                st.write(sentences_df.iloc[link_number]['Spanish'])

                st.subheader("English", divider='orange')
                st.write(sentences_df.iloc[link_number]['English'])

        except:
            container = st.empty()
            container.write("No data loaded.")

            generate_button = st.button("Generate")

            if generate_button:

                container.empty()

                #check_for_sentences = os.path.isfile(sentence_files[week_selection])

                #if check_for_sentences == True:
                    #with open(sentence_files[week_selection], 'r') as f:
                        #sentences_df = pd.read_csv(f, index_col=0)

                    #st.write(sentences_df)
                    ### More TBD

                please_wait_message = st.empty()

                with please_wait_message: 
                    st.warning("You're the first one here. This will take several minutes. Please wait.")

                    all_sentences = []

                    #Sends chunks of vocab to ChatGPT for sentence generation, adds results to list
                    for chunk in process_sentence_chunks(spanish_vocab):
                        generated_sentences = generate_sentences(str(chunk))
                        all_sentences.append("\n" + generated_sentences)

                    #Splitting generated sentences into properly formatted list in preparation for audio creation
                    sentences_df = process_generated_sentences(all_sentences)

                    #Audio generation and saving of DataFrame as CSV
                    sentences_df.loc[:,'Audio'] = sentences_df.apply(google_speech_sentences, df=sentences_df, axis=1)
                    sentences_df.to_csv('./Sentences/' + week_selection + "_" + "final.csv")

                please_wait_message.empty()

                st.rerun()

    if tool_type == "Conversation":

        st.subheader("Chat with GPT", divider='orange')
        st.write("Begin by hitting 'Submit' for the pre-written message.")

        text_box = st.text_area('Type here:', "Hablemos de un tema de su elección.")
        submit_button = st.button("Submit")

        if 'history' not in st.session_state:
            st.session_state['history'] = ""

        if 'conversation_history' not in st.session_state:
            st.session_state['conversation_history'] = []

        if submit_button:
            # Store user input in the session state immediately after the button is pressed
            st.session_state['user_input'] = text_box
            st.session_state['conversation_history'].append(f"User: {st.session_state['user_input']}")

            gpt_response = chat_with_gpt("\n\n".join(st.session_state['conversation_history']))
            st.session_state['conversation_history'].append(f"GPT: {gpt_response}")

            # Update the history
            st.session_state['history'] += f"  \nUser: {st.session_state['user_input']}  \nGPT: {gpt_response}  \n"

        # Display the chat history outside the if block
        write_chat_history()

#Dictionaries of vocab and sentence files
#Update each time new week is added
#root_file_path = "/Users/casey/Documents/PythonProjects/Spanish Learning App/"
vocab_files = {
    "Week 9": "./Vocab/Week 9.csv"
    }

sentence_files = {
    "Week 9": "./Sentences/Week 9_final.csv"
}

#Sets default 'word_index'
if 'word_index' not in st.session_state:
    st.session_state.word_index = 0

#Sets default 'week_selection'
if 'week_selection' not in st.session_state:
    st.session_state.week_selection = "Week 9"

# Dictionary of Spanish-English word pairs
word_pairs = open_vocab_list(st.session_state['week_selection'])

#Regular expression to remove vocab items with parentheses
re_pattern = r'\([^)]*\)'

#Creates list of only Spanish phrases from the vocab dict
spanish_vocab = [re.sub(re_pattern, '', word).strip() for word in word_pairs.keys()]

#Path to sentence audio files
sentence_audio_path = "./Sentences/Audio/"

if __name__ == "__main__":
    main()
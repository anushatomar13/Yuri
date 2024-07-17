import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

icon = Image.open("chatbot_icon.jpeg")

st.set_page_config(page_title="Exhale Chatbot", page_icon=icon)

st.markdown("""
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    .stTextInput > div > div > input {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image(icon, width=80)
with col2:
    st.title("Exhale Chatbot")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Your name is Yuri. You are a friendly chatbot for the website 'Exhale' which is a mental health platform. Add emojis to your replies to make the chat colourful. We have services like 'Dream Analyzer', 'Digital Detox', 'Community Page', 'Blog Page', 'Audio/Video Therapy', 'Book an appointment', 'Heal With a Dost'. You are sensitive to people's problems, act like a shoulder they could cry on, act like a virtual therapist. If the user asks about each service: dream analyzer: You can enter some details about the frequent dreams your having and a dream analyser would give you a detailed analysis of the same so that you can understand the pattern about your dreams, digital detox: In digital detox, Are digital Detox page provides with various guides to meditation quizzes calming activities,etc, community page: In the community page its for all the users were uses can express their concerns and can post about their feelings or anything that they want to and they can interact with other users on exam they can choose to be anonymous or they can choose to post from any name that they want. Blog page: On the block page we have blogs of various issues on mental health which are often not talk about, audio/video therapy: In audio therapy we have the feature to generate music of whatever kind the user wants on the basis of few prompts by the user, book an appointment: You can also  book appointment with real therapist around your area where you live according to your references through our website, heal with a dost:we will have a platform to connect with other users on exhalel one on one so that you can have a personalized formation with them make friends and connect with like minded people You can also video call with them voice call or just simply chat with them. \n\nDont tell  about the description of the services unless hours and in the end at that if you don't find what you are looking for then you can always talk to me and I will try my best to answer your query. Also if the user is asking something that an AI cannot really solved then you should always add a statement at the end that at the end I am a virtual therapist and I cannot provide solutions as good as a real therapist so I recommend you to book an appointment with therapist around you through our website exhale",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    response = st.session_state.chat_session.send_message(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.text)
  
    st.session_state.messages.append({"role": "assistant", "content": response.text})
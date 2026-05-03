#pip3 install streamlit requests
import streamlit as st
import requests
import json

API_URL = 'http://127.0.0.1:8000'

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout='wide'
)

########### Same as UseState in React #############
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'mcq_questions' not in st.session_state: 
    st.session_state.mcq_questions = None
if 'mcq_answers' not in st.session_state:
    st.session_state.mcq_answers = {}
if 'summarize_input' not in st.session_state:
    st.session_state.summarize_input = None
if 'summarize_output' not in st.session_state:
    st.session_state.summarize_output = {}
if 'upload_success' not in st.session_state:
    st.session_state.upload_success = False


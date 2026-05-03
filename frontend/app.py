#pip3 install streamlit requests
### streamlit run app.py
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

######### Sidebar #########
st.sidebar.title('📚 Study Assistant')

st.sidebar.markdown('---')
page = st.sidebar.radio(
    'Navigation', 
    ['💬 Chat', '📄 Upload', '🧠 Generate MCQs', '🔍 Summarize'],
    label_visibility='collapsed'
)

st.sidebar.markdown('---')
st.sidebar.markdown ('**Backend Status**')
try:
    res = requests.get(f'{API_URL}/', timeout=2)
    if res.status_code == 200:
        st.sidebar.success("API Connected")
    else:
        st.sidebar.error("API Connection error")
except:
    st.sidebar.error("API Offline, Start FastAPI first")

st.sidebar.markdown('---')
st.sidebar.markdown('🗑️ Reset Uploads')
try:
    res = requests.delete(f'{API_URL}/reset')
    if res.status_code == 200:
        st.session_state.upload_success = False
        st.sidebar.success("Reset Succcessful")
    else:
        st.sidebar.error('Reset failed')
except:
    st.sidebar.error("Reset Exception")
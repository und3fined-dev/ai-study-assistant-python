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
if 'upload_success' not in st.session_state:
    st.session_state.upload_success = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'summarize_summary' not in st.session_state:
    st.session_state.summarize_summary = None
if 'summarize_keyPoints' not in st.session_state:
    st.session_state.summarize_keyPoints = []
if 'mcq_questions' not in st.session_state: 
    st.session_state.mcq_questions = None
if 'mcq_answers' not in st.session_state:
    st.session_state.mcq_answers = {}


######### Main Page #########
st.markdown("#### 📚 AI Study Assistant")
st.markdown('---')

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
if st.sidebar.button('🗑️ Reset Uploads'):
    try:
        res = requests.delete(f'{API_URL}/reset')
        if res.status_code == 200:
            st.session_state.upload_success = False
            st.sidebar.success("Reset Succcessful")
        else:
            st.sidebar.error('Reset failed')
    except:
        st.sidebar.error("Reset Exception")

################################################# Upload PDF Page ###################################################
if page == '📄 Upload':
    st.title("📄 Upload Study Material")
    st.markdown("Upload any PDF (lecture notes, textbook chapter or any study document.)")

    uploaded_file = st.file_uploader("Choose a PDF File: ", type='PDF')

    if uploaded_file is not None:
        st.info(f'Selected: **{uploaded_file.name}** ({uploaded_file.size//1024} KB)')

        if st.button('Upload and Embed', type='primary'):
            with st.spinner("Uploading and Indexing... this may take a while"):
                try:
                    response = requests.post(
                        f'{API_URL}/upload',
                        files={'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
                        )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.upload_success = True

                        st.success ("PDF uploaded and embedded Successfully")
                        col1, col2, col3 = st.columns(3)
                        col1.metric('File', data['filename'])
                        col2.metric('Total Pages', data['page_count'])
                        col3.metric('Total chunks', data['chunk_count'])
                        st.info("You can now go to **Generate MCQs** or **Chat** to use this PDF.")   
                    else:
                        st.error(f'Upload Failed: {response.json().get("detail", "Unknown Error")}')
                except requests.exceptions.ConnectionError:
                    st.error('Cannot connect to backend. Make sure FastAPI is running.')

    if st.session_state.upload_success:
        st.markdown('---')
        st.success('A document is currently indexed. Ready to use.')

################################################# Chat Page ###################################################
elif page == '💬 Chat':
    st.title('💬 Chat with AI')
    st.markdown('Ask any question, the agent searches your PDF and generates answers')

    ##Load prev chat of the session first
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    ##New Chat
    if prompt := st.chat_input("Ask any question related to your documents..."):
        st.session_state.chat_history.append({
            'role': 'user',
            'content': prompt
        })

        with st.chat_message('user'):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f'{API_URL}/ask',
                    json= {'question': prompt},
                    timeout=60 
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get('answer', "No answer returned.")

                    with st.chat_message('assistant'):
                        st.markdown(answer)

                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': answer
                    })
                else:
                    st.error(f'Failed to generate answer: {response.json().get('detail', 'Unknown error')}')
            except requests.exceptions.ConnectionError:
                st.error('Cannot connect to backend. Make sure FastAPI is running.')
            except requests.exceptions.Timeout:
                st.error('Request timed out — aassistant is taking too long.')

    if st.session_state.chat_history:
        if st.button('🗑️ Clear chat'):
            st.session_state.chat_history = []
            st.rerun()
    
################################################# Summarize Page ###################################################
elif page == '🔍 Summarize':
    st.title("🔍 Summarize Text")
    st.markdown("Paste any lecture notes, chapter or paragraphs to summarize with keypoints")

    ##Input text
    col1, col2 = st.columns([3, 1])
    with col1:
        text = st.text_input('Text', placeholder= 'Paste any text...')
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        summarize_button = st.button('Summarize', type='primary')

    if text.strip() and summarize_button:   
        with st.spinner('Generating summary...'):
            try:
                response = requests.post(
                    f'{API_URL}/summarize',
                    json= {'text': text},
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.summarize_summary = data.get('summary', 'No Summary generated')
                    st.session_state.summarize_keyPoints = data.get('keyPoints', 'No KeyPoints generated')
                else:
                    st.error(f"Failed to generate Summary: {response.json().get('detail', "Unknown Error")}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Make sure FastAPI is running.")
            except requests.exceptions.Timeout:
                st.error('Request timed out — aassistant is taking too long.')
    
    ####### Render Summary Answer ########
    if st.session_state.summarize_summary:
        st.markdown('---')
        st.markdown("### Summary:")
        st.markdown(st.session_state.summarize_summary)
        st.markdown('---')
        st.markdown("#### Key points:")
        for keyPoint in st.session_state.summarize_keyPoints:
            st.markdown(keyPoint)

        ####### Reset button ########
        st.markdown('---')
        if st.button ('🔄 New Summary'):
            st.session_state.summarize_summary = None
            st.session_state.summarize_keyPoints = []
            st.rerun()



################################################# MCQs Page ###################################################
elif page == '🧠 Generate MCQs':
    st.title('🧠 Generate MCQs')
    st.markdown('Ask AI to generate MCQs related to a topic')

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input('Topic', placeholder='e.g. machine learning, operating systems, recursion...')
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        generate_button = st.button('Generate MCQs', type='primary')
    
    if generate_button and topic.strip():
        with st.spinner(f'Generating 10 MCQS on {topic}...'):
            try:
                response = requests.post(
                    f'{API_URL}/generate_mcq',
                    json= {'topic': topic},
                    timeout=60
                )
                if response.status_code==200:
                    st.success(f'MCQs generated successfully on **{topic}**')
                    data = response.json()
                    st.session_state.mcq_questions = data['questions']
                else:
                    st.error(response.json().get('detail', 'MCQs Generation failed.'))
            except requests.exceptions.ConnectionError:
                st.error('Cannot connect to backend. Make sure FastAPI is running.')
            except requests.exceptions.Timeout:
                st.error('Request timed out — aassistant is taking too long.')

    ###### Render MCQs #######
    if st.session_state.mcq_questions:
        st.markdown('---')
        st.markdown('### Questions & Answers')

        for q in st.session_state.mcq_questions:
            st.markdown(f'**Q{q["id"]}. {q["question"]}**')

            for letter, text in q['options'].items():
                is_correct = letter.strip().upper() == q['correct_answer'].strip().upper()
                if is_correct:
                    st.markdown(
                        f'<p style="color: #22c55e; font-weight: 600;">✅ {letter}: {text}</p>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(f'- {letter}: {text}')

            # Explanation
            if q.get('explanation'):
                explanation = q.get('feedback') or q.get('explanation')
                st.markdown(
                    f'<div style="background:#1e293b; border-left: 3px solid #22c55e; '
                    f'padding: 8px 12px; border-radius: 4px; margin: 4px 0 16px 0; '
                    f'font-size: 0.9rem; color: #94a3b8;">'
                    f'💡 {explanation}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown('')

        # Reset button
        st.markdown('---')
        if st.button('🔄 New Quiz'):
            st.session_state.mcq_questions = []
            st.rerun()
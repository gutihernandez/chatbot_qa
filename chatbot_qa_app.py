import os
import streamlit as st
from openai import OpenAI
import logging
import logging.handlers
import time

# Setup Streamlit secrets
log_url = st.secrets["papertrail_url"]
log_port = st.secrets["papertrail_port"]
api_key = st.secrets["OPENAI_API_KEY"]
message_prompt = st.secrets["message_prompt"]

# Configure the OpenAI API client
OpenAI.api_key = api_key
client = OpenAI()

# Setup basic logging configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)
syslog_handler = logging.handlers.SysLogHandler(address=(log_url, int(log_port)))
logger.addHandler(syslog_handler)

# Title of the app
st.title("Kuran Yardımcısı")

# Initialize session state for storing the user input and response
if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "api_response" not in st.session_state:
    st.session_state.api_response = None
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "last_api_call_time" not in st.session_state:
    st.session_state.last_api_call_time = 0.0

@st.cache_data(ttl=3600)
def rate_limited_api_call(client, user_question):
    current_time = time.time()
    time_since_last_call = current_time - st.session_state.last_api_call_time
    if time_since_last_call < 30:
        time.sleep(30 - time_since_last_call)
    st.session_state.last_api_call_time = time.time()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=[
            {"role": "system", "content": message_prompt},
            {"role": "user", "content": user_question[:1000]}
        ]
    )
    return completion

# Input from the user
user_question = st.text_input("Kuran'la alakalı bir soru sorunuz:", value=st.session_state.user_question)

# Check if the input has changed and is non-empty
if user_question and user_question != st.session_state.last_input:
    st.session_state.last_input = user_question

    # Make the rate-limited API call
    completion = rate_limited_api_call(client, user_question)
    
    # Store the API response in session state
    st.session_state.api_response = completion.choices[0].message.content

    # Log the result
    aggregated_result = f"--user_question: {user_question} --answer: {st.session_state.api_response}"
    logger.info(aggregated_result)

# Display the response if available
if st.session_state.api_response:
    st.write("Cevap:", st.session_state.api_response)

# Note for users
st.markdown("**Note:** Cevaplar Yapay Zeka ile üretilmiştir ve her zaman Kuran aracılığıyla teyit edilmelidir.")

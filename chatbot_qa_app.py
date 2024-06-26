import os
import streamlit as st
from openai import OpenAI
import logging
import logging.handlers


papertrail_url=st.secrets["papertrail_url"]
papertrail_port=st.secrets["papertrail_port"]
api_key=st.secrets["OPENAI_API_KEY"]
message_prompt=st.secrets["message_prompt"]
OpenAI.api_key = api_key
client = OpenAI()


# Set up basic logging configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configure the Papertrail handler
syslog_handler = logging.handlers.SysLogHandler(address=(papertrail_url, papertrail_port))
logger.addHandler(syslog_handler)

# Title of the app
st.title("Kuran Yardımcısı")

# Input from the user
user_question = st.text_input("Kuran'la alakalı bir soru sorunuz:")



if user_question:

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens = 1000,
    messages=[
        {"role": "system", "content": message_prompt},
        #{"role": "user", "content": "Tell me which sure in Quran is related to animal sacrifice. Summarize the sure in a single sentence."}
        {"role": "user", "content": user_question}
    ]
    )

    #response = qa_model(question=user_question, context=context)
    #answer = response['answer']
    st.write("Cevap:", completion.choices[0].message.content)
    aggregated_result = "--user_question: " + str(user_question)+ "  --answer: "+ str(completion.choices[0].message.content)
    print(aggregated_result)
    print(type(aggregated_result))
    logger.info(aggregated_result)
else:
    st.write("Kuran'la alakalı bir soru sorunuz:")

# Note for users
st.markdown("**Note:** Cevaplar Yapay Zeka ile üretilmiştir ve her zaman Kuran aracılığıyla teyit edilmelidir.")
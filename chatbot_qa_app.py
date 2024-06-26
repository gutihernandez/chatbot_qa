import os
import streamlit as st
from openai import OpenAI


api_key=st.secrets["OPENAI_API_KEY"]
message_prompt=st.secrets["message_prompt"]
OpenAI.api_key = api_key

client = OpenAI()

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
else:
    st.write("Kuran'la alakalı bir soru sorunuz:")

# Note for users
st.markdown("**Note:** Cevaplar Yapay Zeka ile üretilmiştir ve her zaman Kuran aracılığıyla teyit edilmelidir.")
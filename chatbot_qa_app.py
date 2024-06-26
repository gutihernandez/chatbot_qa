import os
import streamlit as st
from openai import OpenAI


api_key=st.secrets["OPENAI_API_KEY"]
OpenAI.api_key = api_key

client = OpenAI()

# Title of the app
st.title("Quran QA")

# Input from the user
user_question = st.text_input("Ask a question:")



if user_question:

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens = 200,
    messages=[
        {"role": "system", "content": """
         You are a Muslim who knows Quran by memory 
         and a helpful assistant who answers religious questions from holy book Quran. 
         If you give answer, you must give the reference 'sura'. 
         You know that people are sensitive about religion, 
         therefore you only answer if you really know the answer, 
         if you do not know the answer you just say, I do not know. 
         If the question is not related to Quran or if the answer is not in Quran, 
         you do not give answer but you say that the question is unrelated or not in Quran.
         Speak religiously.
         """},
        #{"role": "user", "content": "Tell me which sure in Quran is related to animal sacrifice. Summarize the sure in a single sentence."}
        {"role": "user", "content": user_question}
    ]
    )

    #response = qa_model(question=user_question, context=context)
    #answer = response['answer']
    st.write("Answer:", completion.choices[0].message.content)
else:
    st.write("Please enter a question.")

# Note for users
st.markdown("**Note:** The responses are AI generated and therefore should always be validated with Quran itself.")
import streamlit as st
import requests

st.title('Question Answering App using Streamlit')

# Input textbox for the question
question = st.text_input('Enter your question:', '')

if question:
    # POST the question to the Flask API
    response = requests.post('http://localhost:8080', json={'question': question})
    if response.status_code == 200:
        data = response.json()
        answer = data.get('answer', 'No answer returned.')

        st.subheader('Answer:')
        st.write(answer)
    else:
        st.write("An error occurred while processing the question.")

import streamlit as st
import requests

st.title('Legal Case Question Answering App')

# Document Upload for Indexing
uploaded_text_file = st.file_uploader("Choose files you'd like to index", accept_multiple_files=True)
uploaded_metadata_file = st.file_uploader("Choose the corresponding metadata JSON file", type=["json"])

# Check for unsupported formats
if uploaded_text_file and uploaded_text_file.type != "text/plain":
    st.write("The uploaded text file format is not supported. Please upload a .txt file.")
if uploaded_metadata_file and uploaded_metadata_file.type != "application/json":
    st.write("The uploaded metadata file format is not supported. Please upload a .json file.")

# Indexing After Pressing Confirmation button
if st.button("Index Files"):
    if not uploaded_text_file or not uploaded_metadata_file:
        st.write("Both text and metadata files need to be uploaded before indexing!")
    else:
        files = {
            "text_file": uploaded_text_file.getvalue(),
            "metadata_file": uploaded_metadata_file.getvalue()
        }
        response = requests.post('http://localhost:8080/index', files=files)

        if response.status_code == 200:
            st.write("Successfully indexed the uploaded files!")
        else:
            st.write(f"Failed to index. Reason: {response.text}")


# Input textbox for the question
question = st.text_input('Enter your question:', '')

if question:
    # POST the question to the Flask API
    response = requests.post('http://localhost:8080', json={'question': question})
    if response.status_code == 200:
        data = response.json()
        answer = data.get('answer', 'No answer returned.')
        relevant_score = data.get('score', "No Score")

        st.subheader('Relevant Score:')
        st.write(relevant_score)
        st.subheader('Answer:')
        st.write(answer)
    else:
        st.write("An error occurred while processing the question.")

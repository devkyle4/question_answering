import streamlit as st
import requests

st.title('Legal Case Question Answering App')

# U P L O AD       F E A T U R E

# Document Upload for Indexing
uploaded_files = st.file_uploader("Upload both text and corresponding metadata file", accept_multiple_files=True)

# Indexing After Pressing Confirmation button
if st.button("Index Files"):
    # Filter out text and metadata files
    uploaded_text_files = [f for f in uploaded_files if f.type == "text/plain"]
    uploaded_metadata_files = [f for f in uploaded_files if f.type == "application/json"]

    # Checking if there's any unsupported file format
    unsupported_files = [f for f in uploaded_files if f.type not in ["text/plain", "application/json"]]
    for f in unsupported_files:
        st.write(f"The file {f.name} has an unsupported format. Please upload .txt or .json files.")

    if not uploaded_text_files or not uploaded_metadata_files:
        st.write("Both text and metadata files need to be uploaded before indexing!")

    if len(uploaded_text_files) != 1 or len(uploaded_metadata_files) != 1:
        st.write("Please upload exactly one text file and one metadata file for indexing!")
    else:

        response = requests.post(
            'http://localhost:8080/index',
            files={
                "text_file": uploaded_text_files[0].getvalue(),
                "metadata_file": uploaded_metadata_files[0].getvalue()
            }
        )

        if response.status_code == 200:
            st.write("Successfully uploaded files for indexing!")
        else:
            st.write(f"Failed to index. Reason: {response.text}")


# A S K I N G     Q U E S T I O NS     F E A T U R E

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

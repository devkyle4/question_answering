import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Legal Case Question Answering App")

host_url = os.environ.get("API_BASE")
index_url = f"{host_url}/index"


def attempt_connection(url, delay=5):
    while True:
        try:
            res = requests.get(url)
            if res.status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(delay)
    return False


# U P L O A D       F E A T U R E

# Document Upload for Indexing
uploaded_files = st.file_uploader(
    "Upload both text and corresponding metadata file", accept_multiple_files=True
)

# Indexing After Pressing Confirmation button
if st.button("Index Files"):
    # Filter out text and metadata files
    uploaded_text_files = [f for f in uploaded_files if f.type == "text/plain"]
    uploaded_metadata_files = [
        f for f in uploaded_files if f.type == "application/json"
    ]

    # Checking if there's any unsupported file format
    unsupported_files = [
        f for f in uploaded_files if f.type not in ["text/plain", "application/json"]
    ]
    for f in unsupported_files:
        st.write(
            f"The file {f.name} has an unsupported format. Please upload .txt or .json files."
        )

    if len(uploaded_text_files) != 1 or len(uploaded_metadata_files) != 1:
        st.write("Both text and metadata files need to be uploaded before indexing!")
    else:
        try:
            response = requests.post(
                index_url,
                files={
                    "text_file": uploaded_text_files[0].getvalue(),
                    "metadata_file": uploaded_metadata_files[0].getvalue(),
                },
            )
            # print(response)
            response.raise_for_status()
            if response.status_code == 200:
                st.write("Successfully uploaded files for indexing!")
            else:
                st.write(f"Failed to index. Reason: {response.text}")

                # Attempt to connect to the Flask service at startup
                with st.spinner("Attempting to connect to Flask service..."):
                    is_connected = attempt_connection(host_url)
                    if not is_connected:
                        st.error(
                            "Failed to connect to the Flask service after multiple attempts."
                        )
                    else:
                        st.success("Successfully connected to the Flask service!")
        except requests.RequestException as e:
            st.write(f"An error occurred: {e}")

# A S K I N G     Q U E S T I O N S     F E A T U R E

# Input textbox for the question
question = st.text_input("Enter your question:", "")
if st.button("Answer"):
    if question:
        with st.spinner("Fetching Response"):
            try:
                response = requests.post(host_url, json={"question": question})

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer returned.")
                    relevant_score = data.get("score", "No Score")

                    st.subheader("Relevant Score:")
                    st.write(relevant_score)
                    st.subheader("Answer:")
                    st.write(answer)
                else:
                    st.write(
                        f"Failed to process the question. Server response: {response.text}"
                    )

            except requests.RequestException as e:  # Handle request exceptions
                st.write(f"An error occurred while contacting the Flask service: {e}")

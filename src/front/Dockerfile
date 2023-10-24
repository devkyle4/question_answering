# Use an official Python runtime as the base image
FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt


# Copy the content of the app directory into the container
COPY ./gui.py /app/

EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "gui.py"]

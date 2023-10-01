# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./app/requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the 'app' directory contents into the container at /app
COPY ./app/ /app/

# Make port 5000 available to the world outside this container (for Flask)
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]

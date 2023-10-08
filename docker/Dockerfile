# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory (which should be /app in the context of the Dockerfile) into the container at /app
COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY .. /app/

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy supervisord config file
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose Flask and Streamlit ports
EXPOSE 5000 8501

# Run supervisord when the container launches
CMD ["/usr/bin/supervisord"]



































# # Set the working directory in the container to /app
# WORKDIR /app

# # Copy the requirements file into the container at /app
# COPY ../requirements.txt /app/

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r /app/requirements.txt

# # Copy the 'app' directory contents into the container at /app
# COPY ./app /app


# # In Dockerfile
# ENV DATABASE_URL='devkyle'
# ENV PASSWORD=123456

# # Run app.py when the container launches
# CMD ["python", "/app/app.py"]

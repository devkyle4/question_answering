# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app


# Install supervisord
RUN dpkg-reconfigure tzdata && \
    apt-get update && apt-get install -y supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/log/supervisor && \
    chown -R nobody:nogroup /var/log/supervisor

# Copy the current directory (which should be /app in the context of the Dockerfile) into the container at /app
COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY .. /app/

# Set permissions for nobody
RUN chown -R nobody:nogroup /app && \
    chmod -R 755 /app
    
# Copy supervisord config file
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose Flask and Streamlit ports
EXPOSE 5000 8501

# Run supervisord when the container launches
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]




































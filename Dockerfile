# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY health-check.py requirements.txt /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Disable output buffering for real-time logging
ENV PYTHONUNBUFFERED=1

# Set the default command to open a shell (or bash)
CMD ["bash"]
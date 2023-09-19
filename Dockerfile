# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Install system dependencies required for pyodbc
RUN apt-get update -y \
    && apt-get install -y unixodbc-dev \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]

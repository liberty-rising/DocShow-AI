# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++ \
    && apt-get clean

# Install Microsoft ODBC Driver for SQL Server
RUN apt-get update && apt-get install -y curl gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Set the working directory in the container
WORKDIR /app/frontend

# Copy the frontend directory contents into the container
COPY . /app/frontend

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Set PYTHONPATH
ENV PYTHONPATH=/app/frontend

# Run app.py when the container launches
CMD ["streamlit", "run", "--server.fileWatcherType=poll", "app.py"]


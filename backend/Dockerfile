# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app/backend

# Copy the backend directory contents into the container
COPY . /app/backend

# Install curl, postgres client, and build-essential
RUN apt-get update && \
    apt-get install -y curl postgresql-client build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy wait-for.sh into the container
COPY wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your app using uvicorn
CMD ["/wait-for.sh", "postgres_db", "5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

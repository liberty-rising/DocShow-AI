# docshowai

This repository contains a Streamlit app. Below are the instructions to build and run the Docker image.

## Prerequisites

- Docker installed on your machine

## Build and Run Using Docker

### Instructions

1. Open a terminal (for Linux/Mac users) or Command Prompt (for Windows users) and navigate to the repository directory.

2. Build the Docker image:

    ```bash
    docker build -t docshowai .
    ```

3. Run the Docker container:

    ```bash
    docker run -p 8501:8501 docshowai
    ```

After following these steps, you should be able to access the Streamlit app at [http://localhost:8501/](http://localhost:8501/).

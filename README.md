# docshowai

This repository contains a Streamlit frontend and a FastAPI backend. Below are instructions for setting up the development environment using Docker Compose.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine

## Build and Run Using Docker Compose

### Instructions

1. Open a terminal (for Linux/Mac users) or Command Prompt (for Windows users) and navigate to the repository root directory.

2. Build and start the services defined in `docker-compose.yml`:

    ```bash
    docker-compose up --build
    ```

After executing these commands, you should be able to access:

- The Streamlit app at [http://localhost:8501/](http://localhost:8501/)
- The FastAPI backend at [http://localhost:8000/](http://localhost:8000/)

### Stopping Services

To stop the services, press `Ctrl+C` in the terminal where `docker-compose up` is running, or run:

```bash
docker-compose down
```

### Logs

To view logs for the services, you can run:

```bash
docker-compose logs
```

You can also view logs for individual services:

```bash
docker-compose logs frontend
docker-compose logs backend
```

That's it! You're now up and running with your development environment.

# docshowai

This repository contains a React frontend and a FastAPI backend. Below are instructions for setting up the development environment using Docker Compose.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine

## Setup Process

### Creating SSL/TLS Certificates for Local Development

Generate locally-trusted SSL/TLS certificates using `mkcert`.

1. Install `mkcert`.

2. Create a directory/folder called `certs/` in the project's root.

3. Generate certificates `localhost.key` and `localhost.crt` within `certs/` using `mkcert`.

### Building the Docker containers

1. Open a terminal (for Linux/Mac users) or Command Prompt (for Windows users) and navigate to the repository root directory.

2. Build and start the services defined in `docker-compose.yml`:

    ```bash
    docker-compose up --build
    ```

### Building the frontend

1. Open a terminal (for Linux/Mac users) or Command Prompt (for Windows users) and navigate to the repository root directory.

2. Navigate inside the frontend directory, and run `npm install`.

    ```bash
    cd frontend/
    npm install
    ```

3. Once the packages finish installing, run `npm run dev`.

    ```bash
    npm run dev
    ```

### Success

After executing these commands, you should be able to access:

- The React frontend at [https://127.0.0.1/](https://127.0.0.1/)
- The FastAPI backend at [https://127.0.0.1/api](https://127.0.0.1/api)

### Stopping Services

To stop the services, press `Ctrl+C` in the terminals where `docker-compose up` and React are running.

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

### Database Migrations

For any change to the schema you should create a database migration using alembic.

Generate a new alembic version:
```bash
cd backend
alembic revision -m "{description of revision}"
```

Your revision will be located within `/backend/alembic/versions`
Edit the generated revision file with your changes, make sure to specify both upgrade and downgrade function for reverse compatibility.
After making changes to your revision file, apply them using:
```bash
alembic upgrade head
```

If you deleted volumes and recreated the containers, you must point alembic to the latest version.
This is because the backend automatically creates the latest schema for you.
You can do this by running the following command:
```bash
alembic stamp head
```

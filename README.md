# Refund Flask App

## Overview

This project is a Flask-based application designed for handling payments and refunds. It integrates with Celery for task management and uses Kafka for message brokering. The system supports automatic refund processing and periodic status checks. It also includes endpoints for managing and inquiring about transactions and refunds.

## Features

- **Automatic Refunds**: Automatically processes refunds for failed transactions.
- **Periodic Status Checks**: Uses Celery Beat to run tasks every 30 minutes to check transaction and refund statuses.
- **Transaction Management**: Provides endpoints to list, get details, and filter transactions.
- **Refund Management**: Provides endpoints to get refund details and filter refunds.

## Installation

1. **Set up a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:

    Set environment variables for configuration, e.g.:

    ```sh
    FLASK_APP=app.py
    FLASK_ENV=development
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0
    KAFKA_BOOTSTRAP_SERVERS=localhost:9092
    REFUND_TOPIC=refund_requests
    ```

## Database Setup

1. **Create the database**:

    ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
    ```

## Running the Application

1. **Start the Flask application**:

    ```sh
    python app.py
    ```

2. **Start the Celery worker**:

    ```sh
    celery -A celery_worker.celery worker --loglevel=info
    ```

3. **Start the Celery Beat scheduler**:

    ```sh
    celery -A celery_worker.celery beat --loglevel=info
    ```
   

## API Endpoints

### Transactions

- **List All Transactions**

    ```
    GET /transactions
    ```

    Query parameters:
    - `status`: Filter transactions by status.

- **Get Specific Transaction**

    ```
    GET /transactions/<transaction_id>
    ```

- **List Failed Transactions**

    ```
    GET /transactions/failed
    ```

- **List Incomplete Transactions**

    ```
    GET /transactions/incomplete
    ```

### Refunds

- **Get Refund by ID**

    ```
    GET /refund/<refund_id>
    ```

- **List All Refunds**

    ```
    GET /refunds
    ```

- **Filter Refunds**

    ```
    GET /refunds/filter
    ```

    Query parameters:
    - `transaction_id`: Filter refunds by transaction ID.
    - `status`: Filter refunds by status.

## Docker Setup

**Build Docker image**:

```sh
docker build -t abrnoc-refund-task .
docker run -d -p 5000:5000 --name abrnoc-refund-task-container abrnoc-refund-task
docker run -d --name celery_worker --link abrnoc-refund-task-container abrnoc-refund-task celery -A celery_worker.celery worker --loglevel=info
docker run -d --name celery_beat --link abrnoc-refund-task-container abrnoc-refund-task celery -A celery_worker.celery beat --loglevel=info 
```
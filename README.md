# Workflow Management 🚀

Welcome to Workflow Management, a robust API for managing workflows utilizing the FastAPI framework.

## Installation 🛠️

### Using Docker 🐳

1. First, make sure you have Docker and Docker Compose installed. If not, install them by following the respective instructions for your operating system.

2. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/kostomeister/fastapi-workflow-management.git
    ```

3. Navigate to the project directory:

    ```bash
    cd fastapi-workflow-management
    ```

4. Start Docker Compose:

    ```bash
    docker-compose up --build
    ```

5. After successful launch, the API will be available at `http://127.0.0.1:8000`.

### Without Docker ⚙️

1. Install Python version 3.8 or newer.

2. Clone the repository and navigate to the project directory:

    ```bash
    git clone https://github.com/kostomeister/fastapi-workflow-management.git
    cd fastapi-workflow-management
    ```
3. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # for Unix/Mac
    # or
    venv\Scripts\activate  # for Windows
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run migrations:
 ```bash
   alembic upgrade head
 ```

6. Run the server:

    ```bash
    uvicorn main:app --reload
    ```

7. After successful launch, the API will be available at `http://127.0.0.1:8000`.

## Testing 🧪

The project utilizes the pytest library for testing. To run tests, execute the following command in the project's root directory:

```bash
pytest tests
```

This will run all tests from the `tests` directory and display the results in the terminal.

## Contributions 🤝

If you have any suggestions or you've encountered an issue, please create a new issue or submit a pull request. Your contributions are valuable to me!

Thank you for your interest in this project! 🚀
# Software Testing Automation Project

A Python-based software testing project that demonstrates API development, automated testing, input validation, authentication, product management, and code-quality checks.

## Overview

This project contains two FastAPI services: an Authentication Service for user registration, login, and JWT-based authentication, and a Product Service for product management and stock operations. It includes unit tests, API tests, load-testing scripts, and automated code-quality checks to improve software reliability.

## Features

- **Authentication Service:** User registration, login, password verification, and JWT token generation.
- **Product Service:** Create, retrieve, and update products.
- **Stock Management:** Reserve and release product stock with quantity validation.
- **Input Validation:** Pydantic models validate incoming API requests.
- **Automated Testing:** Unit and API tests using pytest.
- **Load Testing:** Locust scripts for authentication and product endpoints.
- **Code Quality:** Flake8 linting and Mypy static type checking.
- **Database Integration:** SQLite with SQLAlchemy ORM.
- **Continuous Integration:** GitHub Actions workflow for automated quality checks.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | REST API development |
| SQLAlchemy | Database access and ORM |
| SQLite | Local database storage |
| Pydantic | Request validation and response schemas |
| JWT | Token-based authentication |
| pytest | Automated testing |
| HTTPX | API testing |
| Locust | Load testing |
| Flake8 | Code style and linting |
| Mypy | Static type checking |
| Git and GitHub | Version control and source hosting |
| GitHub Actions | Continuous integration |

## Project Structure

```text
softwaretesting/
├── load/
│   ├── locust_auth.py
│   └── locust_product.py
├── services/
│   ├── auth_service/
│   │   ├── __init__.py
│   │   └── main.py
│   └── product_service/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── api/
│   │   ├── test_auth_api.py
│   │   └── test_product_api.py
│   └── unit/
│       ├── test_auth_unit.py
│       └── test_product_unit.py
├── .github/
│   └── workflows/
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

The exact files and workflow configuration may vary according to your repository.

## Prerequisites

Install the following before running the project:

- Python 3.11 or compatible version
- pip
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/software-testing-automation.git
cd software-testing-automation
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository URL.

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` does not contain the development tools, install them with:

```bash
pip install pytest httpx flake8 mypy black ruff locust
```

## Running the Services

Run the services in separate terminals from the project root.

### Authentication Service

```bash
uvicorn services.auth_service.main:app --reload --port 8001
```

API documentation:

`http://127.0.0.1:8001/docs`

### Product Service

```bash
uvicorn services.product_service.main:app --reload --port 8002
```

API documentation:

`http://127.0.0.1:8002/docs`

The services use separate SQLite databases for local development.

## API Endpoints

### Authentication Service

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a user |
| POST | `/login` | Authenticate a user and obtain a token |
| GET | `/me` | Retrieve the authenticated user's details |

### Product Service

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products` | Create a product |
| GET | `/products/{pid}` | Retrieve a product |
| PUT | `/products/{pid}` | Update a product |
| POST | `/products/{pid}/reserve` | Reserve product stock |
| POST | `/products/{pid}/release` | Release product stock |

Use the interactive Swagger documentation at `/docs` to explore and test the endpoints.

## Automated Testing

Run all tests from the project root:

```bash
python -m pytest
```

Run unit tests only:

```bash
python -m pytest tests/unit
```

Run API tests only:

```bash
python -m pytest tests/api
```

## Code Quality Checks

Run Flake8:

```bash
flake8
```

Run Mypy:

```bash
mypy services
```

Format Python code using Black:

```bash
black load services tests
```

Automatically fix supported Ruff issues:

```bash
ruff check --fix load services tests
```

Review automatic changes and rerun the tests before committing.

## Load Testing with Locust

The project includes Locust scripts for authentication and product endpoints.

Start a load test using the relevant script:

```bash
locust -f load/locust_auth.py
```

Or:

```bash
locust -f load/locust_product.py
```

Open the Locust web interface shown in the terminal, configure the target host and load parameters, and run the test against a service that is already running.

Use a local development environment for load testing. Avoid generating unnecessary traffic against production systems.

## Continuous Integration

GitHub Actions can run automated checks whenever code is pushed to the repository. The workflow can include:

- Flake8 linting
- Mypy static type checking
- pytest automated tests

Check the **Actions** tab in GitHub to review workflow results and diagnose failed checks.

## Security Considerations

- Use a strong secret supplied through environment variables for JWT signing.
- Do not commit API keys, passwords, `.env` files, or private credentials.
- Use a dedicated password-hashing algorithm, such as Argon2, before production deployment.
- SQLite databases and test data should not contain real user information.
- Configure production settings separately from local development.

## Future Enhancements

- Expand API test coverage for edge cases and invalid requests.
- Add test coverage reporting.
- Improve authentication and password security.
- Add more load-testing scenarios and performance reports.
- Integrate test results and quality reports into the CI pipeline.
- Add containerized deployment and environment-specific configuration.

## Author

**Skanda Sharma**

## License

Add a license file if you intend to distribute or reuse this project under a specific license.

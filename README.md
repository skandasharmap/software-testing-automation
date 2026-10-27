# STQA Complex Project — Microservices QA Suite (Auth + Product)

A realistic **microservices-style** project to demonstrate **Software Testing & Quality Assurance** across layers:
- Two services (FastAPI): **Auth Service** (JWT) and **Product Service** (inventory & reservations)
- **Unit, API/Integration, Contract, Performance, Security, and CI** coverage
- **Static analysis** (flake8, mypy), **security scan** (bandit), **coverage**
- **Docs**: Test Plan, Strategy, RTM, Test Cases, Risks, Defects, Test Report
- **Postman collection** and **GitHub Actions** CI pipeline

> Default DB: SQLite (file). Optional Postgres wiring shown in `docker-compose.yml` (extend as needed).

## Quick Start (local, no Docker)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
. .venv/bin/activate
pip install -r requirements.txt

# Run services (in separate shells or use &)
uvicorn services.auth_service.main:app --reload --port 8001
uvicorn services.product_service.main:app --reload --port 8002
```

## Run All Tests + Linters
```bash
pytest -q
flake8
mypy services
bandit -r services -q
coverage run -m pytest && coverage html
```

## Endpoints
- Auth: `POST /register`, `POST /login`, `GET /me` (Bearer token)
- Product: `POST /products`, `GET /products/{id}`, `PUT /products/{id}`,
  `POST /products/{id}/reserve`, `POST /products/{id}/release`

## Load Tests (Locust)
```bash
locust -f load/locust_auth.py --host=http://localhost:8001
locust -f load/locust_product.py --host=http://localhost:8002
```

## CI
GitHub Actions workflow in `.github/workflows/ci.yml` runs: install, lint, unit/API tests, coverage upload (artifact).

---

**Educational intent:** This project is intentionally scoped to be runnable locally while still covering *advanced QA practices*.

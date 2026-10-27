# Test Plan — STQA Complex Project (Auth + Product)

## 1. Scope
- **Auth Service**: register, login (JWT), me
- **Product Service**: product CRUD, stock reserve/release

## 2. Test Types
- Unit, API/Integration, Contract (Pydantic schema), Performance (Locust), Security (Bandit + ZAP baseline), Static (flake8, mypy).

## 3. Test Levels & Environments
- Dev (SQLite), CI (GitHub Actions), Perf (Local Locust).

## 4. Entry/Exit
- Entry: Services up, migrations applied.
- Exit: 95%+ critical tests pass; no Sev‑1/Sev‑2 open; coverage ≥ 80% (target).

## 5. Tools
pytest, httpx, coverage, locust, bandit, flake8, mypy, Postman/ZAP.

## 6. Risks
- Race conditions on stock updates (mitigated by tests).
- Token replay (mitigated via short expiry; for prod add revocation).

## 7. Deliverables
- Test cases, RTM, defect log, test report, CI artifacts.

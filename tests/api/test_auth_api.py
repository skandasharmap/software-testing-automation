import httpx, pytest, asyncio
from threading import Thread
import uvicorn
from services.auth_service.main import app as auth_app

@pytest.fixture(scope="session", autouse=True)
def _run_auth():
    config = uvicorn.Config(auth_app, host="127.0.0.1", port=8001, log_level="error")
    server = uvicorn.Server(config)
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    yield

@pytest.mark.asyncio
async def test_register_and_login_flow():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8001") as c:
        r = await c.post("/register", json={"email":"a@b.com","name":"Asha","password":"secret1"})
        assert r.status_code in (201, 400)  # if rerun, user may exist
        r = await c.post("/login", json={"email":"a@b.com","password":"secret1"})
        assert r.status_code == 200
        token = r.json()["access_token"]
        r = await c.get("/me", headers={"authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json()["email"] == "a@b.com"

from threading import Thread

import httpx
import pytest
import uvicorn

from services.product_service.main import app as product_app


@pytest.fixture(scope="session", autouse=True)
def _run_product():
    config = uvicorn.Config(product_app, host="127.0.0.1", port=8002, log_level="error")
    server = uvicorn.Server(config)
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    yield


@pytest.mark.asyncio
async def test_product_crud_and_reservations():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8002") as c:
        r = await c.post(
            "/products", json={"name": "Notebook", "price": 99.0, "stock": 3}
        )
        assert r.status_code == 201
        pid = r.json()["id"]
        # reserve ok
        r = await c.post(f"/products/{pid}/reserve", params={"qty": 2})
        assert r.status_code == 200
        assert r.json()["stock"] == 1
        # reserve conflict
        r = await c.post(f"/products/{pid}/reserve", params={"qty": 2})
        assert r.status_code == 409
        # release
        r = await c.post(f"/products/{pid}/release", params={"qty": 1})
        assert r.status_code == 200
        assert r.json()["stock"] == 2

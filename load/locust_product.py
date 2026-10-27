import random

from locust import HttpUser, between, task


class ProductUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        r = self.client.post(
            "/products", json={"name": "LoadItem", "price": 10.0, "stock": 100}
        )
        self.pid = r.json().get("id", 1)

    @task
    def reserve_release(self):
        qty = random.randint(1, 3)
        self.client.post(f"/products/{self.pid}/reserve", params={"qty": qty})
        self.client.post(f"/products/{self.pid}/release", params={"qty": qty})

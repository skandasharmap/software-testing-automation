from locust import HttpUser, task, between

class AuthUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.post("/register", json={"email":"locust@load.com","name":"Load","password":"secret1"})
        r = self.client.post("/login", json={"email":"locust@load.com","password":"secret1"})
        if r.status_code == 200:
            self.token = r.json().get("access_token")
        else:
            self.token = None

    @task
    def me(self):
        if self.token:
            self.client.get("/me", headers={"authorization": f"Bearer {self.token}"})

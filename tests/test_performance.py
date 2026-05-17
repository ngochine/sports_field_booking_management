from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def get_home(self):
        self.client.get("/")

    @task(1)
    def get_field(self):
        self.client.get("/fields")


    @task(1)
    def get_fields(self):
        self.client.get("/fields/1")

    def on_start(self):
        response = self.client.post(
            "/api/auth/login",
            json={
                "username": "ngoctrinh",
                "password": "Trinh2005@"
            }
        )

    @task
    def profile(self):
        self.client.get("/profile")

    @task
    def get_bookings(self):
        self.client.get("/bookings")
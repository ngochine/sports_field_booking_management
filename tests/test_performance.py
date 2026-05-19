from locust import HttpUser, task, between
from datetime import date, timedelta
import random


class GuestFlow(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_home(self):
        self.client.get("/", name="Home")

    @task(3)
    def get_fields(self):
        self.client.get("/fields", name="Fields")

    @task(2)
    def get_field_detail(self):
        self.client.get("/fields/1", name="Field Detail")


class UserFlow(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.username = f"user_{random.randint(1000, 999999)}"
        self.password = "Test@123"

        self.client.post(
            "/api/auth/register",
            json={
                "username": self.username,
                "password": self.password,
                "confirm": self.password
            },
            name="Register"
        )

        self.client.post(
            "/api/auth/login",
            json={
                "username": self.username,
                "password": self.password
            },
            name="Login"
        )

    @task(2)
    def profile(self):
        self.client.get("/profile", name="Profile")

    @task(3)
    def get_fields(self):
        self.client.get("/fields", name="Fields")

    @task(2)
    def get_field_detail(self):
        self.client.get("/fields/1", name="Field Detail")

    @task(2)
    def get_bookings(self):
        self.client.get("/bookings", name="Bookings")

    def on_stop(self):
        self.client.post("/api/auth/logout", name="Logout")
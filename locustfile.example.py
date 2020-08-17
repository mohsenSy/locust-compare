"""Sample locust file for initial testsing."""
from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    """A class that represents one user to test the server."""

    wait_time = between(5, 15)
    host = "https://google.com"

    @task
    def index(self):
        """Run a single test on main page."""
        self.client.get("/")

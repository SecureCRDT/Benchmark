from locust import HttpUser, task, tag, constant, FastHttpUser
import random


class GCounter(FastHttpUser):
    wait_time = constant(0)

    def on_start(self):
        # Setup initial counter value
        self.client.get("/api/update?value=" + str(1), name="on_start")

    @task
    @tag("update")
    def update(self):
        self.client.get("/api/update?value=" + str(1), name="/api/update?value=[value]")

    @task
    @tag("query")
    def query(self):
        self.client.get("/api/query")

    @task
    @tag("merge")
    def merge(self):
        self.client.get("/api/merge")

    @task
    @tag("propagate")
    def propagate(self):
        self.client.get("/api/propagate")

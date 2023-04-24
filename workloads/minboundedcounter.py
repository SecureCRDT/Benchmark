import random

from locust import HttpUser, task, tag, constant, FastHttpUser


class MinBoundedCounter(FastHttpUser):
    wait_time = constant(0)

    def on_start(self):
        # Setup initial value
        self.client.get("/api/update?value=" + str(1) + "&op=setup", name="on_start_setup")
        self.client.get("/api/update?value=" + str(2 ** 15) + "&op=inc", name="on_start_inc")

    @task
    @tag("update")
    def increment(self):
        self.client.get("/api/update?value=" + str(1) + "&op=inc", name="/api/update?value=[value]&op=inc")

    @task
    @tag("update")
    def decrement(self):
        self.client.get("/api/update?value=" + str(1) + "&op=dec", name="/api/update?value=[value]&op=dec")

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

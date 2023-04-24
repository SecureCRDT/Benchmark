import random

from locust import HttpUser, task, tag, constant, FastHttpUser


class PNCounter(FastHttpUser):
    wait_time = constant(0)

    def on_start(self):
        # Setup initial Register value
        # Set a middle int value that can be incremented or decremented without much risk of overflowing the shares.
        # However, it should not be a problem if the shares overflow.
        value = 2 ** 15
        self.client.get("/api/update?value=" + str(value) + "&op=inc", name="on_start")

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

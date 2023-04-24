from locust import HttpUser, task, tag, constant, FastHttpUser
import random


class Register(FastHttpUser):
    wait_time = constant(0)

    def on_start(self):
        # Setup initial Register value
        register_value = random.randint(0, 2 ** 30)
        self.client.get("/api/update?value=" + str(register_value), name="on_start")

    @task
    @tag("update")
    def insert(self):
        register_value = random.randint(0, 2 ** 30)
        self.client.get("/api/update?value=" + str(register_value), name="/api/update?value=[value]")

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

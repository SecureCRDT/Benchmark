from locust import task, tag, constant, FastHttpUser, events
import random
import os


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--set-size", type=str,
                        env_var="SET_SIZE", default="0", help="It's working")



class Set(FastHttpUser):
    wait_time = constant(0)

    def on_start(self):
        set_size_str = self.environment.parsed_options.set_size
        print(f"my_argument={set_size_str}")
        set_size = int(set_size_str)
        # Setup initial value
        for _ in range(0, set_size):
            value = random.randint(0, 2 ** 30)
            self.client.get("/api/update?value=" + str(value), name="on_start")

    @task
    @tag("update")
    def update(self):
        value = random.randint(0, 2 ** 30)
        self.client.get("/api/update?value=" + str(value), name="/api/update?value=[value]")
        
    @task
    @tag("query")
    def exists(self):
        value = random.randint(0, 2 ** 30)
        # The performance of this operation will significantly decrease over time during the benchmark.
        self.client.get("/api/query?op=exists&value=" + str(value), name="/api/query?value=[value]&op=exists")

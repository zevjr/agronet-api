from locust import HttpUser, LoadTestShape


class SuiteTest(HttpUser):
    tasks = [
        # Aqui deve ser chamado todos os modulos que serão executados com locust.
    ]


class TestShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 1000, "spawn_rate": 20},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

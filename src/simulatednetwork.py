import random

from src.load_balancing import LoadBalancingAlgorithm


class Task:
    def __init__(self, duration, load, birth_time):
        self.duration = duration
        self.load = load
        self.birth_time = birth_time
        self.end_time = birth_time + duration

    def __repr__(self):
        return f"Task(duration={self.duration}, load={self.load}, birth_time={self.birth_time})"


class Processor:
    def __init__(self, uuid, max_load, gen_frequency, load_balancing_algorithm):
        self.uuid = uuid
        self.max_load = max_load
        self.gen_frequency = gen_frequency
        self.load_balancing_algorithm = load_balancing_algorithm

        self.current_load = 0
        self.tasks = []
        self.load_history = []
        self.migrations = 0
        self.queries = 0

    def generate_task(self, task_parameters: dict):
        task = Task(task_parameters["duration"], task_parameters["load"], task_parameters["birth_time"])
        # determine which processor will handle the task

    def assign_task(self):
        pass


class Network:
    def __init__(self, node_amount, processor_parameters, lb_algorithm, seed):
        self.seed = seed
        self.lb_algorithm: LoadBalancingAlgorithm = lb_algorithm
        self.processors = []
        self.create_processors(node_amount, processor_parameters)
        self.time = 0

    def create_processors(self, node_amount, processor_parameters):
        avg_p_max_load = processor_parameters["average_max_load"]
        p = processor_parameters["p"]
        avg_task_gen_frequency = processor_parameters["average_task_gen_frequency"]
        for _ in range(node_amount):
            _max_load = avg_p_max_load + avg_p_max_load * (random.random() - 0.5) / 4
            _task_frequency = abs(random.normalvariate(avg_task_gen_frequency, 3*avg_task_gen_frequency))
            self.processors.append(Processor(_, _max_load, _task_frequency, self.lb_algorithm))

    def step(self):
        pass
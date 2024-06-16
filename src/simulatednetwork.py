import random


class Task:
    def __init__(self, duration, load):
        self.duration = duration
        self.load = load

    def __repr__(self):
        return f"Task(duration={self.duration}, load={self.load})"


class Processor:
    def __init__(self, network, uuid, max_load, gen_frequency, max_queries, p, r, load_balancing_algorithm):
        self.uuid = uuid
        self.max_load = max_load
        self.willing_to_work_weight = 2**max_load
        self.gen_frequency = gen_frequency
        self.load_balancing_algorithm = load_balancing_algorithm
        self.neighbours = []
        self.network = network

        self.overload_time = 0
        self.max_queries = max_queries
        self.p = p
        self.r = r
        self.current_load = 0
        self.tasks = []
        self.load_history = []
        self.migrations = 0
        self.queries = 0
        self.save_counter = 0

    def generate_task(self, task_parameters: dict):
        min_duration, max_duration = task_parameters["task_duration_range"]
        min_load, max_load = task_parameters["task_load_range"]

        task = Task(random.randint(min_duration, max_duration), random.randint(min_load, max_load))
        self.assign_task(task)

    def assign_task(self, task):
        selected_processor = self.load_balancing_algorithm.select_processor(self)
        selected_processor.add_task(task)

    def add_task(self, task):
        self.tasks.append(task)
        self.current_load += task.load

    def remove_task(self, task):
        self.network.ongoing_tasks -= 1
        self.tasks.remove(task)
        self.current_load -= task.load

    def step(self):
        # print("Current load: {}, max load: {}".format(self.current_load, self.max_load))
        self.save_counter += 1
        if self.save_counter >= 10:
            self.load_history.append(self.get_load_ratio())
            self.save_counter = 0

        if self.current_load > self.max_load:
            self.overload_time += 1

        for task in self.tasks:
            task.duration -= 1
            if task.duration <= 0:
                self.remove_task(task)

    def get_load_ratio(self):
        return self.current_load / self.max_load

    def __repr__(self):
        return (f"Processor {self.uuid}: max_load = {self.max_load: .2f}, gen_frequency = {self.gen_frequency: .2f}")

    def __str__(self):
        return f"Processor {self.uuid}: max_load = {self.max_load: .2f}, gen_frequency = {self.gen_frequency: .2f}"


class SimulatedNetwork:
    def __init__(self, node_amount, processor_parameters, task_parameters):
        # self.seed = seed
        self.node_amount = node_amount
        self.algorithm = None
        self.processors = []
        self.ongoing_tasks = 0
        self.tasks_left = 0
        self.processor_parameters = processor_parameters
        self.task_parameters = task_parameters
        self.time = 0

    def create_processors(self, node_amount):
        avg_p_max_load = self.processor_parameters["average_max_load"]
        avg_task_gen_frequency = self.processor_parameters["average_task_gen_frequency"]
        p = self.processor_parameters["p"]
        r = self.processor_parameters["r"]
        max_queries = self.processor_parameters["max_queries"]

        for _ in range(node_amount):
            _max_load = avg_p_max_load + avg_p_max_load * (random.random() - 0.5) / 4
            _task_frequency = abs(random.normalvariate(avg_task_gen_frequency, 10 * avg_task_gen_frequency) + avg_task_gen_frequency)
            self.processors.append(Processor(self, _, _max_load, _task_frequency, max_queries, p, r, self.algorithm))

        for proc in self.processors:
            proc.neighbours = [_ for _ in self.processors if _ is not proc]

    def try_task_generation(self):
        if self.tasks_left <= 0:
            return
        for proc in self.processors:
            if proc.gen_frequency * random.betavariate(2, 5) > 50:
                proc.generate_task(self.task_parameters)
                self.ongoing_tasks += 1
                self.tasks_left -= 1

    def step(self):
        self.time += 1
        self.try_task_generation()

        for proc in self.processors:
            self.algorithm.steal_task(proc)

        for proc in self.processors:
            proc.step()

    def get_state(self):
        return [proc.get_load_ratio() for proc in self.processors]

    def __repr__(self):
        return "\n".join(str(proc) for proc in self.processors)

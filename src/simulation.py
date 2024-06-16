from src.simulatednetwork import SimulatedNetwork


class Simulation:
    def __init__(self):
        self.network = None

    def setup_network(self, algorithm, tasks_left):
        #self.network.seed = seed
        self.network.lazy_algorithm = algorithm
        self.network.tasks_left = tasks_left
        self.network.algorithm = algorithm
        self.network.create_processors(self.network.node_amount)

    def simulate_algorithm(self, algorithm, network, tasks_left):
        self.network = network
        self.setup_network(algorithm, tasks_left)
        algorithm.network = network

        while self.network.tasks_left > 0 or self.network.ongoing_tasks > 0:
            self.network.step()

        queries = sum(proc.queries for proc in self.network.processors)
        migrations = sum(proc.migrations for proc in self.network.processors)
        avg_load = sum(sum(proc.load_history) / len(proc.load_history) for proc in self.network.processors) / len(self.network.processors)
        avg_overload_time = sum(proc.overload_time for proc in self.network.processors) / len(self.network.processors)
        print(f"Algorithm: {algorithm.__class__.__name__}")
        print(f"Queries: {queries}")
        print(f"Migrations: {migrations}")
        print(f"Average load: {avg_load * 100:.2f}%")
        print(f"Average overload time (% of simulation time): {avg_overload_time / self.network.node_amount / self.network.time * 100:.2f}%")
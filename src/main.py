import copy
import random

from src.simulation import Simulation

if __name__ == "__main__":
    from src.simulatednetwork import SimulatedNetwork
    from src.load_balancing import LazyStudentAlgorithm, AmbitiousStudentAlgorithm, HelpfulStudentAlgorithm

    SEED = 1337

    min_task_duration = 5
    max_task_duration = 20
    min_task_load = 3
    max_task_load = 20
    node_amount = 50
    task_amount = 2500
    processor_parameters = {
        "average_max_load": 100,
        "max_queries": 20,
        "p": 0.6,
        "r": 0.2,
        "average_task_gen_frequency": 40,  # 10 is min rational value
    }
    task_parameters = {
        "task_load_range": (min_task_load, max_task_load),
        "task_duration_range": (min_task_duration, max_task_duration)
    }

    # Load balancing algorithm
    lazy_algorithm = LazyStudentAlgorithm()
    ambitious_algorithm = AmbitiousStudentAlgorithm()
    helpful_algorithm = HelpfulStudentAlgorithm()

    network = SimulatedNetwork(node_amount, processor_parameters, task_parameters)
    print(network)

    simulation = Simulation()
    random.seed(SEED)
    simulation.simulate_algorithm(lazy_algorithm, copy.deepcopy(network), 2500)
    random.seed(SEED)
    simulation.simulate_algorithm(ambitious_algorithm, copy.deepcopy(network), 2500)
    random.seed(SEED)
    simulation.simulate_algorithm(helpful_algorithm, copy.deepcopy(network), 2500)

import random

from src.simulatednetwork import Processor, SimulatedNetwork


class LoadBalancingAlgorithm:
    def __init__(self):
        self.network = None

    def query_processors(self, processors: list, z):
        queries = 0
        while z > 0:
            queries += 1
            processor = random.choices(processors, weights=[proc.willing_to_work_weight for proc in processors])[0]
            if processor.get_load_ratio() < processor.p:
                return processor, queries
            z -= 1
        return None, queries

    def select_processor(self, origin_node: Processor):
        pass

    def steal_task(self, origin_node: Processor):
        pass


class LazyStudentAlgorithm(LoadBalancingAlgorithm):
    def select_processor(self, origin_node: Processor):
        proc, queries = self.query_processors(origin_node.neighbours, origin_node.max_queries)
        if proc is None:
            proc = origin_node
        else:
            origin_node.migrations += 1
        proc.queries += queries
        return proc


class AmbitiousStudentAlgorithm(LoadBalancingAlgorithm):
    def select_processor(self, origin_node: Processor):
        if origin_node.get_load_ratio() < origin_node.p:
            proc, queries = origin_node, 0
        else:
            proc, queries = self.query_processors(origin_node.neighbours, origin_node.max_queries)
            if proc is None:
                proc = origin_node
            else:
                proc.migrations += 1
        proc.queries += queries
        return proc


class HelpfulStudentAlgorithm(LoadBalancingAlgorithm):
    def steal_task(self, origin_node: Processor):
        if origin_node.get_load_ratio() > origin_node.r:
            return
        # for neighbour in random.choices(origin_node.neighbours,
        #                                 weights=[proc.willing_to_work_weight for proc in origin_node.neighbours])[0:origin_node.max_queries % len(origin_node.neighbours)]:
        z = origin_node.max_queries
        while z > 0:
            z -= 1
            origin_node.queries += 1
            processor = random.choices(origin_node.neighbours, weights=[proc.willing_to_work_weight for proc in origin_node.neighbours])[0]
            if processor.get_load_ratio() > processor.p and len(processor.tasks) > 0:
                task = random.choice(processor.tasks)
                origin_node.add_task(task)
                processor.remove_task(task)
                origin_node.migrations += 1
                return

    def select_processor(self, origin_node: Processor):
        if origin_node.get_load_ratio() < origin_node.p:
            proc, queries = origin_node, 0
        else:
            proc, queries = self.query_processors(origin_node.neighbours, origin_node.max_queries)
            if proc is None:
                proc = origin_node
            else:
                proc.migrations += 1
        proc.queries += queries
        self.steal_task(origin_node)
        return proc

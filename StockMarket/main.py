import time
import resource

from algorithms import GreedyAlgorithm, DynamicProgramingAlgorithm

from investor_structure import Item, ItemWithSlots

from algorithms import DynamicProgramingOptimizedAlgorithm
from utils import ResultWriter, Parser, get_args, Algorithm

if __name__ == "__main__":
    alg, input_file, output_file = get_args()

    item_class = Item
    if alg == Algorithm.GREEDY:
        algorithm = GreedyAlgorithm
    elif alg == Algorithm.DYNAMIC:
        algorithm = DynamicProgramingAlgorithm
    elif alg == Algorithm.DYNAMIC_OPTIMAL:
        algorithm = DynamicProgramingOptimizedAlgorithm
        item_class = ItemWithSlots
    else:
        raise ValueError("Algorithm can be one of: {}, {}, {}"
                         .format(Algorithm.GREEDY, Algorithm.DYNAMIC, Algorithm.DYNAMIC_OPTIMAL))

    investor, items = Parser.parse(input_file, item_class)

    start_time = time.time()

    algorithm(investor, items).calculate()

    duration = time.time() - start_time

    print('Duration is {:.2f} ms'.format(duration * 1000))
    print('Memory usage: {} KB'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))

    ResultWriter.write(investor, output_file)



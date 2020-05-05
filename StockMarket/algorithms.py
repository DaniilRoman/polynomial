import sys
from numba import jit, jitclass, int32
import numpy as np

import warnings

warnings.filterwarnings("ignore")


class StockMarketAlgorithm:
    def __init__(self, investor, items):
        self.investor = investor
        self.items = items


class GreedyAlgorithm(StockMarketAlgorithm):

    def calculate(self):
        while len(self.items) > 0:
            max_value = -sys.maxsize - 1
            max_item = None
            for item in self.items:
                if item.total_reward > max_value:
                    max_value = item.total_reward
                    max_item = item
            self.investor.add_item_or_not(max_item)
            self.items.remove(max_item)

        self.investor.total_reward = self.investor.get_total_reward()


class DynamicProgramingAlgorithm(StockMarketAlgorithm):

    def calculate(self):
        investor_money = self.investor.s_money
        best_rewards = [[0] * (investor_money + 1) for _ in range(len(self.items) + 1)]

        for current_item_index, (item) in enumerate(self.items, 1):
            reward = item.total_reward
            cost = item.total_cost

            prev_item_index = current_item_index - 1
            for current_money in range(investor_money + 1):
                if cost > current_money:
                    best_rewards[current_item_index][current_money] = best_rewards[prev_item_index][current_money]
                else:
                    best_rewards[current_item_index][current_money] = max(best_rewards[prev_item_index][current_money],
                                                                          best_rewards[prev_item_index][
                                                                              current_money - cost] + reward)

        available_money = investor_money
        for item_number in reversed(range(1, len(self.items) + 1)):
            if best_rewards[item_number][available_money] != best_rewards[item_number - 1][available_money]:
                self.investor.add_item((self.items[item_number - 1]))
                available_money -= self.items[item_number - 1].total_cost

        self.investor.items.reverse()
        self.investor.total_reward = best_rewards[len(self.items)][investor_money]


class DynamicProgramingOptimizedAlgorithm(StockMarketAlgorithm):

    def calculate(self):
        numba_items = []
        for item in self.items:
            numba_items.append(NumbaItem(item.total_cost, item.total_reward))
        result, selected_indexes = dynamic_programming_with_numba(numba_items, self.investor.s_money)
        self.investor.total_reward = result
        self.investor.items = [self.items[i] for i in selected_indexes]


spec = [
    ('weight', int32),
    ('value', int32),
]


@jitclass(spec)
class NumbaItem:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value


@jit
def dynamic_programming_with_numba(items, investor_money):
    n = len(items)
    best_rewards = np.zeros(shape=(n + 1, investor_money + 1), dtype=int)

    for current_item_index in range(1, n + 1):
        prev_item_index = current_item_index - 1
        cost = items[prev_item_index].weight
        reward = items[prev_item_index].value
        for current_money in range(investor_money + 1):
            if cost > current_money:
                best_rewards[current_item_index, current_money] = best_rewards[prev_item_index, current_money]
            else:
                best_rewards[current_item_index, current_money] = max(best_rewards[prev_item_index, current_money],
                                                                      best_rewards[
                                                                          prev_item_index, current_money - cost] + reward)
    taken = []

    available_money = investor_money
    for i in range(n, 0, -1):
        if best_rewards[i][available_money] != best_rewards[i - 1][available_money]:
            taken.append(i - 1)
            available_money -= items[i - 1].weight

    taken.reverse()

    return int(best_rewards[n, investor_money]), taken

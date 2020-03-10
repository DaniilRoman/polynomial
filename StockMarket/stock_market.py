# 1 item       = 1000 $
# 1 day off    = 1 $
# after period = 1000 $

# item:
#      - name
#      - price [% by 1000 $]

# N - days
# name; price; count - is known

# from 0 to M items every days
# S - money count

# can buy only whole pack

import os


class Item:
    def __init__(self, day, name, price, count):
        self.day = day
        self.name = name
        self.price = price
        self.count = count
        self.totalCost = price * 10 * count
        self.totalReward = (1000 * count + (day + 30) * self.count) - self.totalCost


class Investor:
    def __init__(self, n_days, m_items, s_money):
        self.n_days = n_days
        self.m_items = m_items
        self.s_money = s_money
        self.items = []

    def add_item(self, item):
        if self.s_money - item.totalCost >= 0:
            self.items.append(item)
            self.s_money -= item.totalCost

    def get_total_reward(self):
        total_reward = 0
        for item in self.items:
            total_reward += item.totalReward
        return total_reward


class GreedyAlgorithm:
    def __init__(self, investor, items):
        self.investor = investor
        self.items = items

    def calculate(self):
        while len(self.items) > 0:
            max_value = 0
            max_item = None
            for item in self.items:
                if item.totalReward > max_value:
                    max_value = item.totalReward
                    max_item = item
            self.investor.add_item(max_item)
            self.items.remove(max_item)


class SolverStrategy:
    def __init__(self, investor, items):
        self.alg = GreedyAlgorithm(investor, items)

    def calculate(self):
        self.alg.calculate()
        return self.alg.investor.get_total_reward()


class Parser:
    @staticmethod
    def parse(file_path):
        with open(file_path) as fp:
            n_days, m_items, s_money = fp.readline().split()
            investor = Investor(int(n_days), int(m_items), int(s_money))
            items = []
            for line in fp:
                day, name, price, count = line.split()
                items.append(Item(int(n_days) - int(day), str(name), float(price), int(count)))
            return investor, items

    @staticmethod
    def get_text(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        return data


class ResultWriter:
    @staticmethod
    def write(solver):
        result_str = ResultWriter.get_result_str(solver)

        with open(os.path.join('result_files', 'test_result.txt'), 'w') as file:
            file.write(result_str)

    @staticmethod
    def get_result_str(solver):
        result = solver.calculate()
        investor = solver.alg.investor
        result_str = str(result) + '\n'
        result_str += '\n'.join(['{} {} {} {}'.format(investor.n_days - i.day, i.name, i.price, i.count)
                                 for i in investor.items])
        result_str += '\n'
        return result_str

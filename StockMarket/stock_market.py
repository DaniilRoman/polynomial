import os


class Item:
    def __init__(self, day, name, price, count):
        self.day = day
        self.name = name
        self.price = price
        self.count = count
        self.total_cost = int(price * 10 * count)
        self.total_reward = (1000 * count + (day + 30) * self.count) - self.total_cost


class Investor:
    def __init__(self, n_days, m_items, s_money):
        self.n_days = n_days
        self.m_items = m_items
        self.s_money = s_money

        self.items = []
        self.total_reward = None

    def add_item(self, item):
        if self.s_money - item.total_cost >= 0:
            self.items.append(item)
            self.s_money -= item.total_cost

    def get_total_reward(self):
        if self.total_reward is not None:
            return self.total_reward
        total_reward = 0
        for item in self.items:
            total_reward += item.total_reward
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
                if item.total_reward > max_value:
                    max_value = item.total_reward
                    max_item = item
            self.investor.add_item(max_item)
            self.items.remove(max_item)


class DynamicProgramingAlgorithm:
    def __init__(self, investor, items):
        self.investor = investor
        self.items = items

    def calculate(self):
        def knapsack(W, wt, val, n):
            K = [[0 for x in range(W + 1)] for x in range(n + 1)]

            for i in range(n + 1):
                for w in range(W + 1):
                    if i == 0 or w == 0:
                        K[i][w] = 0
                    elif wt[i - 1] <= w:
                        K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]],
                                      K[i - 1][w])
                    else:
                        K[i][w] = K[i - 1][w]
            # K[n][W]
            return K

        def find_ans(k, s):
            if _best_reword_matrix[k][s] == 0:
                return
            if _best_reword_matrix[k - 1][s] == _best_reword_matrix[k][s]:
                find_ans(k - 1, s)
            else:
                find_ans(k - 1, s - total_cost[k])
                _answer_indexes.append(k)

        total_reward = [item.total_reward for item in self.items]
        total_cost = [item.total_cost for item in self.items]
        investor_money = self.investor.s_money
        count_papers = len(total_cost)

        _best_reword_matrix = knapsack(investor_money, total_cost, total_reward, count_papers)
        _answer_indexes = []

        find_ans(count_papers, investor_money)

        self.investor.total_reward = _best_reword_matrix[count_papers][investor_money]
        for i in _answer_indexes[-1::-1]:
            self.investor.items.append(self.items[i - 1])


class SolverStrategy:
    def __init__(self, alg):
        self.alg = alg

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

        with open(os.path.join('result_files', 'test_result_actual.txt'), 'w') as file:
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


def calculate_wrapper(file_path):
    investor, items = Parser.parse(file_path)
    solver = SolverStrategy(GreedyAlgorithm(investor, items))
    ResultWriter.write(solver)

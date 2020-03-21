import os

import numpy as np

from stock_market import get_actual_result_path


def calculate_greedy(file_path):
    days = np.empty([0], dtype=np.uint8)
    names = np.empty([0], dtype='<U64')
    prices = np.empty([0], dtype=np.float32)
    counts = np.empty([0], dtype=np.uint8)
    total_costs = np.empty([0], dtype=np.float32)
    total_rewards = np.empty([0], dtype=np.float32)

    with open(file_path) as fp:
        n_days, m_items, s_money = fp.readline().split()
        investor_stuff = np.array([int(n_days), int(m_items), int(s_money)])
        for line in fp:
            day, name, price, count = line.split()

            day = investor_stuff[0] - int(day)
            count = int(count)
            total_cost = float(price) * 10 * count

            days = np.append(days, day)
            names = np.append(names, name)
            prices = np.append(prices, price)
            counts = np.append(counts, count)
            total_costs = np.append(total_costs, total_cost)
            total_rewards = np.append(total_rewards, (1000 * count + (day + 30) * count) - total_cost)

    best_days = np.empty([0], dtype=np.uint8)
    best_names = np.empty([0], dtype='<U64')
    best_prices = np.empty([0], dtype=np.float32)
    best_counts = np.empty([0], dtype=np.uint8)

    result_rewords = 0

    while days.size > 0:
        max_i = np.argmax(total_rewards)

        if investor_stuff[2] - total_costs[max_i] >= 0:
            best_days = np.append(best_days, days[max_i])
            best_names = np.append(best_names, names[max_i])
            best_prices = np.append(best_prices, prices[max_i])
            best_counts = np.append(best_counts, counts[max_i])

            investor_stuff[2] = investor_stuff[2] - total_costs[max_i]

            result_rewords += total_rewards[max_i]

        days = np.delete(days, max_i)
        names = np.delete(names, max_i)
        prices = np.delete(prices, max_i)
        counts = np.delete(counts, max_i)
        total_costs = np.delete(total_costs, max_i)
        total_rewards = np.delete(total_rewards, max_i)

    result_str = str(int(result_rewords)) + '\n'
    result_str += '\n'.join(
        ['{} {} {} {}'.format(investor_stuff[0] - best_days[i], best_names[i], best_prices[i], best_counts[i])
         for i in range(best_days.size-1, -1, -1)])
    result_str += '\n'
    with open(get_actual_result_path(), 'w') as file:
        file.write(result_str)

    return result_str

def calculate_dynamic_programing(file_path):
    days = np.empty([0], dtype=np.uint8)
    names = np.empty([0], dtype='<U64')
    prices = np.empty([0], dtype=np.float32)
    counts = np.empty([0], dtype=np.uint8)
    total_costs = np.empty([0], dtype=np.int32)
    total_rewards = np.empty([0], dtype=np.float32)

    with open(file_path) as fp:
        n_days, m_items, s_money = fp.readline().split()
        investor_stuff = np.array([int(n_days), int(m_items), int(s_money)])
        for line in fp:
            day, name, price, count = line.split()

            day = investor_stuff[0] - int(day)
            count = int(count)
            total_cost = int(float(price) * 10 * count)

            days = np.append(days, day)
            names = np.append(names, name)
            prices = np.append(prices, price)
            counts = np.append(counts, count)
            total_costs = np.append(total_costs, total_cost)
            total_rewards = np.append(total_rewards, (1000 * count + (day + 30) * count) - total_cost)

    def knapsack(W, wt, val, n):
        K = np.zeros((n + 1, W + 1), dtype=int)

        for i in range(n + 1):
            for w in range(W + 1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif wt[i - 1] <= w:
                    K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
                else:
                    K[i][w] = K[i - 1][w]
        return K

    def find_ans(k, s):
        if _best_reword_matrix[k][s] == 0:
            return
        if _best_reword_matrix[k - 1][s] == _best_reword_matrix[k][s]:
            find_ans(k - 1, s)
        else:
            find_ans(k - 1, s - total_costs[k])
            _answer_indexes.append(k)

    count_papers = len(total_costs)

    _best_reword_matrix = knapsack(investor_stuff[2], total_costs, total_rewards, count_papers)
    _answer_indexes = []

    find_ans(count_papers - 1, investor_stuff[2] - 1)

    result_rewords = _best_reword_matrix[count_papers][investor_stuff[2]]

    result_str = str(int(result_rewords)) + '\n'
    result_str += '\n'.join(
        ['{} {} {} {}'.format(investor_stuff[0] - days[i], names[i], prices[i], counts[i])
         for i in range(len(_answer_indexes))])
    result_str += '\n'
    with open(get_actual_result_path(), 'w') as file:
        file.write(result_str)

    return result_str


if __name__ == "__main__":
    calculate_greedy(os.path.join('test_files', 'first_test.txt'))

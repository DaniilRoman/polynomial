import unittest
import os
from statistics import mean

from stock_market import Investor, SolverStrategy, Item, Parser, \
    ResultWriter, calculate_wrapper, GreedyAlgorithm, DynamicProgramingAlgorithm
from stock_market_optim import calculate

import time


class StockMarketTest(unittest.TestCase):

    def test_with_constructing(self):
        items = [Item(3, '1', 80, 2), Item(2, '2.1', 70, 3), Item(2, '2.2', 90, 4)]
        investor = Investor(4, 2, 3800)
        solver = SolverStrategy(GreedyAlgorithm(investor, items))

        self.assertEqual(
            1462,
            solver.calculate())

    def test_with_parsing(self):
        investor, items = Parser.parse(os.path.join('test_files', 'first_test.txt'))
        solver = SolverStrategy(GreedyAlgorithm(investor, items))

        self.assertEqual(
            1462,
            solver.calculate())

    def test_with_writing_result_greedy(self):
        self._run_with_writing_result(GreedyAlgorithm)

    def test_with_writing_result_dynamic_programing(self):
        self._run_with_writing_result(DynamicProgramingAlgorithm)

    def _run_with_writing_result(self, alg):
        investor, items = Parser.parse(os.path.join('test_files', 'first_test.txt'))
        solver = SolverStrategy(alg(investor, items))
        ResultWriter.write(solver)

        actual = Parser.get_text(os.path.join('result_files', 'test_result_actual.txt'))
        expected = Parser.get_text(os.path.join('result_files', 'test_result_expected.txt'))

        self.assertEqual(
            expected,
            actual)

    def test_with_writing_result_optimal(self):
        calculate(os.path.join('test_files', 'first_test.txt'))
        expected = Parser.get_text(os.path.join('result_files', 'test_result_expected.txt'))
        actual = Parser.get_text(os.path.join('result_files', 'test_result_actual.txt'))

        self.assertEqual(
            expected,
            actual)

    def test_performance_once_run(self):
        file_path = os.path.join('test_files', 'first_test.txt')
        n = 1000
        time_1 = []
        time_2 = []

        for i in range(n):
            start_time = time.time()
            calculate_wrapper(file_path)
            time_1.append(time.time() - start_time)
            # print("--- %s seconds ---" % (time.time() - start_time))

        for i in range(n):
            start_time = time.time()
            calculate(file_path)
            time_2.append(time.time() - start_time)

        print("--- %s seconds ---" % mean(time_1))
        print("--- %s seconds ---" % mean(time_2))


    # def test_gfg_imlpementation(self):
    #
    #     def knapsack(W, wt, val, n):
    #         K = [[0 for x in range(W + 1)] for x in range(n + 1)]
    #
    #         for i in range(n + 1):
    #             for w in range(W + 1):
    #                 if i == 0 or w == 0:
    #                     K[i][w] = 0
    #                 elif wt[i - 1] <= w:
    #                     K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
    #                 else:
    #                     K[i][w] = K[i - 1][w]
    #         # K[n][W]
    #         return K
    #
    #     def find_ans(k, s):
    #         if _best_reword_matrix[k][s] == 0:
    #             return
    #         if _best_reword_matrix[k - 1][s] == _best_reword_matrix[k][s]:
    #             find_ans(k - 1, s)
    #         else:
    #             find_ans(k - 1, s - total_cost[k])
    #             _answer_indexes.append(k)
    #
    #     total_reward = [60, 100, 120, 500, 200, 15]  # to MAX
    #     total_cost = [2, 3, 3, 4, 5, 4]  # <= investor_money
    #     investor_money = 10
    #     count_papers = len(total_cost)
    #
    #     _best_reword_matrix = knapsack(investor_money, total_cost, total_reward, count_papers)
    #     _answer_indexes = []
    #
    #     find_ans(count_papers, investor_money)
    #     best_reword = _best_reword_matrix[count_papers][investor_money]
    #
    #     print(best_reword)
    #     print(_answer_indexes)


if __name__ == '__main__':
    unittest.main()

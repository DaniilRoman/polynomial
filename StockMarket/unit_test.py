import unittest
import os
from statistics import mean

from stock_market import Investor, SolverStrategy, Item, Parser, ResultWriter
from stock_market_optim import calculate

import time

from StockMarket.stock_market import calculate_wrapper


class StockMarketTest(unittest.TestCase):

    def test_with_constructing(self):
        items = [Item(3, '1', 80, 2), Item(2, '2.1', 70, 3), Item(2, '2.2', 90, 4)]
        investor = Investor(4, 2, 3800)
        solver = SolverStrategy(investor, items)

        self.assertEqual(
            1462,
            solver.calculate())

    def test_with_parsing(self):
        investor, items = Parser.parse(os.path.join('test_files', 'first_test.txt'))
        solver = SolverStrategy(investor, items)

        self.assertEqual(
            1462,
            solver.calculate())

    def test_with_writing_result(self):
        investor, items = Parser.parse(os.path.join('test_files', 'first_test.txt'))
        solver = SolverStrategy(investor, items)
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

if __name__ == '__main__':
    unittest.main()

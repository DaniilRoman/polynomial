import unittest
import os

from StockMarket.stock_market import Investor, SolverStrategy, Item, Parser, ResultWriter


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

        actual = ResultWriter.get_result_str(solver)
        expected = Parser.get_text(os.path.join('result_files', 'test_result.txt'))

        self.assertEqual(
            expected,
            actual)

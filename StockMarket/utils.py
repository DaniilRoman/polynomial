import getopt
import os
import sys

from investor_structure import Investor


class Parser:
    @staticmethod
    def parse(file_path, item_class):
        with open(file_path) as fp:
            n_days, m_items, s_money = fp.readline().split()
            investor = Investor(int(n_days), int(m_items), int(s_money))
            items = []
            for line in fp:
                day, name, price, count = line.split()
                items.append(item_class(int(n_days) - int(day), str(name), float(price), int(count)))
            return investor, items

    @staticmethod
    def get_text(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        return data

def get_actual_result_path():
    return os.path.join('result_files', 'test_result_actual.txt')

class ResultWriter:
    @staticmethod
    def write(investor, file_path=get_actual_result_path()):
        result_str = str(investor.total_reward) + '\n'
        result_str += '\n'.join(['{} {} {} {}'.format(int(investor.n_days - i.day), i.name, float(i.price), int(i.count))
                                 for i in investor.items])
        result_str += '\n'

        with open(file_path, 'w') as file:
            file.write(result_str)


class Algorithm:
    GREEDY = "greedy"
    DYNAMIC = "dynamic"
    DYNAMIC_OPTIMAL = "dynamic_optimal"

def get_args():
    argv = sys.argv[1:]
    alg = None
    input_file = None
    output_file = None
    try:
        opts, args = getopt.getopt(argv, "a:i:o:")
    except getopt.GetoptError:
        print('main.py -a <algorithm> -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-a':
            alg = arg
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    if alg is None:
        print("Please set algorithm with `-a` argument: {}, {}, {}"
              .format(Algorithm.GREEDY, Algorithm.DYNAMIC, Algorithm.DYNAMIC_OPTIMAL))
        exit(2)
    if input_file is None:
        print("Please set input file with `-i` argument")
        exit(2)
    if output_file is None:
        print("Please set output file with `-o` argument")
        exit(2)

    return alg, input_file, output_file
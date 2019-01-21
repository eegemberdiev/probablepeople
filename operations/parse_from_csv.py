from __future__ import print_function

import os

from parserator import data_prep_utils

from operations.heplers.csv_handler import read_matrix_from_csv
from probablepeople import parse
from settings import BASE_DIR


def launch():
    full_name_file = os.path.join(BASE_DIR, 'name_data/unlabeled/filtered_names.csv')
    # full_name_file = os.path.join(BASE_DIR, 'name_data/unlabeled/courthouse.csv')
    # full_name_file = os.path.join(BASE_DIR, 'name_data/unlabeled/dev_courthouse_grantor.csv')
    # outer_file = os.path.join(BASE_DIR, 'name_data/labeled/dev_courthouse_grantor.xml')
    outer_file = os.path.join(BASE_DIR, 'name_data/labeled/courthouse.xml')
    # import importlib
    # module = importlib.import_module('parse_from_csv')
    import probablepeople
    for row_string in read_matrix_from_csv(full_name_file):
        labeled_sequence = parse(row_string[0])
        data_prep_utils.appendListToXMLfile([labeled_sequence], probablepeople, outer_file)
        # print(labeled_sequence)


if __name__ == '__main__':
    launch()

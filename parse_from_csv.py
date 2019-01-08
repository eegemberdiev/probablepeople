from __future__ import print_function

import csv
import os

from parserator import data_prep_utils

from probablepeople import parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# def measure_accuracy(dev_dataset):
#     failed = 0
#     for labeled_sting in dev_dataset:
#         labels_true = get_labels_from_list_of_tuple(labeled_sting)
#         dev_string = get_dev_string_from_list_of_tuples(labeled_sting)
#         parsed = parse(dev_string)
#         labels_pred = [token[1] for token in parsed]
#         if labels_pred == labels_true:
#             print(dev_string, "...ok")
#         else:
#             failed += 1
#             print("*" * 40)
#             print(dev_string, "...INCORRECT PARSING")
#             print("pred: ", labels_pred)
#             print("true: ", labels_true)
#             print("-" * 40)
#         # if labels_pred != labels_true:
#         #     failed += 1
#         #     # print("*" * 40)
#         #     # print(dev_string, "...INCORRECT PARSING")
#         #     # print("pred: ", labels_pred)
#         #     # print("true: ", labels_true)
#         #     # print("-" * 40)
#
#     print("Failed", failed, "out of", len(dev_dataset), "strings")
#     print("Accuracy", (len(dev_dataset) - failed) / float(len(dev_dataset)) * 100, "%")

def read_from_csv(path_to_file):
    with open(path_to_file) as csv_file:
        matrix = []
        reader = csv.reader(csv_file)
        for row_string in reader:
            # yield row_string
            matrix.append(row_string)
        return matrix


def launch():
    full_name_file = os.path.join(BASE_DIR, 'name_data/unlabeled/filtered_names.csv')
    # full_name_file = os.path.join(BASE_DIR, 'name_data/unlabeled/courthouse.csv')
    # full_name_file = os.path.join(BASE_DIR, 'name_data/unlabeled/dev_courthouse_grantor.csv')
    # outer_file = os.path.join(BASE_DIR, 'name_data/labeled/dev_courthouse_grantor.xml')
    outer_file = os.path.join(BASE_DIR, 'name_data/labeled/courthouse.xml')
    # import importlib
    # module = importlib.import_module('parse_from_csv')
    import probablepeople
    for row_string in read_from_csv(full_name_file):
        labeled_sequence = parse(row_string[0])
        data_prep_utils.appendListToXMLfile([labeled_sequence], probablepeople, outer_file)
        # print(labeled_sequence)


if __name__ == '__main__':
    launch()

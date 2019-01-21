# Module to measure classification accuracy
# Reads data from csv file

import os
import re
from collections import OrderedDict

from parserator import data_prep_utils

import probablepeople
from operations.heplers.csv_handler import read_dict_from_csv
from probablepeople import parse
from settings import BASE_DIR


def equally_tagged(labels_true, labels_pred):
    for predicted_sequence in labels_pred:
        name_parsed = predicted_sequence[0]
        label = {
            'MiddleInitial': 'MiddleName',
            'FirstInitial': 'GivenName',
        }.get(predicted_sequence[1], predicted_sequence[1])
        if label in labels_true.values():
            value_index = list(labels_true.values()).index(label)
            true_name = labels_true.get((list(labels_true.keys())[value_index]))
            if true_name and name_parsed not in true_name:
                return False
    return True


def filter_empty_values(labeled_sequence):
    keys_of_empty_values = []
    for key in labeled_sequence.keys():
        if not key:
            keys_of_empty_values.append(key)
    for key in keys_of_empty_values:
        del labeled_sequence[key]
    return labeled_sequence


def relable_initials(labeled_sequence):
    matching_labels = {
        'GivenName': 'FirstInitial',
        'MiddleName': 'MiddleInitial',
    }
    keys_of_initials = []
    for key in labeled_sequence.keys():
        if re.search(r'^\w{1}((\.(.)*)|((\s)*))$', key):
            keys_of_initials.append(labeled_sequence[key])
    labeled_sequence = OrderedDict(
        [(k, matching_labels[v]) if v in matching_labels.keys() and v in keys_of_initials else (k, v) for k, v in
         labeled_sequence.items()])
    return labeled_sequence


def preprocess_labeled_sequence(labeled_sequence):
    labeled_sequence = filter_empty_values(labeled_sequence)
    labeled_sequence = relable_initials(labeled_sequence)
    return labeled_sequence


def write_to_file(labeled_sequence, module, path_to_file):
    labeled_sequence = preprocess_labeled_sequence(labeled_sequence)
    data_prep_utils.appendListToXMLfile([labeled_sequence.items()], module, path_to_file)


def measure_accuracy(dev_dataset, outer_file=None):
    """Measures accuracy of model against given dev_dataset

    :param outer_file: file to save failed predictions
    :param dev_dataset: a matrix with following fields in concrete order

    Given name | middle name | Surname | Full name
    John       |  Richard    |  Doe    | John Richard Doe
    """

    failed = 0
    for labeled_row in dev_dataset:
        try:
            labels_true = OrderedDict([
                (labeled_row['GivenName'], 'GivenName'),
                (labeled_row['MiddleName'], 'MiddleName'),
                (labeled_row['Surname'], 'Surname')
            ])
        except IndexError:
            print(labeled_row)
            raise IndexError()
        dev_string = labeled_row['FullName']
        labels_predicted = parse(dev_string)
        if equally_tagged(labels_true, labels_predicted):
            print(dev_string, "...ok")
        else:
            failed += 1
            print("*" * 40)
            print(dev_string, "...INCORRECT PARSING")
            print("pred: ", labels_predicted)
            print("true: ", labels_true)
            print("-" * 40)
            if outer_file:
                write_to_file(labels_true, probablepeople, outer_file)

    print("Failed", failed, "out of", len(dev_dataset), "strings")
    print("Accuracy", (len(dev_dataset) - failed) / float(len(dev_dataset)) * 100, "%")


def launch():
    labeled_csv_file = os.path.join(BASE_DIR, 'mahara-full-names/labeled_csvs/people.csv')
    # outer_file = os.path.join(BASE_DIR, 'mahara-full-names/labeled_xml/people1.xml')

    dict_csv = read_dict_from_csv(labeled_csv_file)
    measure_accuracy(dict_csv)


if __name__ == '__main__':
    launch()

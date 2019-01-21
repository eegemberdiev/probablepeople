from __future__ import print_function

import os
from xml.etree import cElementTree as ElementTree

from operations.heplers.xml_converter import XmlListConfig
from probablepeople import parse
from settings import BASE_DIR


# Read from xml file labeled data and measure accuracy

def get_dev_string_from_list(labeled_string):
    dev_string = ' '.join(map(str, [word[0] for word in labeled_string]))
    return dev_string


def get_dev_string_from_dict(labeled_dict):
    dev_string = ' '.join(map(str, [word for word in labeled_dict.values()]))
    return dev_string


def get_dev_string_from_list_of_tuples(labeled_list_of_tuples):
    dev_string = ' '.join(map(str, [token[1] for token in labeled_list_of_tuples]))
    return dev_string


def get_labels_from_list(list_dev_string):
    labels = [label[1] for label in list_dev_string]
    return labels


def get_labels_from_list_of_tuple(list_of_tuple_dev_string):
    labels = [token[0] for token in list_of_tuple_dev_string]
    return labels


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


def labels_are_equal(labels_pred, labels_true, critical_labels=None):
    if len(labels_true) != len(labels_pred):
        # raise Exception('Length of labels must be equal')
        return False

    if critical_labels is None:
        return labels_pred == labels_true

    for index, true_label in enumerate(labels_true):
        if true_label in critical_labels and labels_pred[index] != true_label:
            return False
    return True


def count_hamming_loss(labels_pred, labels_true, critical_labels):
    true_predictions = 0.0
    for index, true_label in enumerate(labels_true):
        try:
            if true_label in critical_labels and labels_pred[index] == true_label:
                true_predictions += 1
        except ValueError:
            continue
    return true_predictions / len(set(critical_labels).intersection(set(labels_true)))


def measure_accuracy_given_surname(dev_dataset, **kwargs):
    dataset_length = len(dev_dataset)
    failed_critical = 0
    hamming_loss = 0.0
    for labeled_sting in dev_dataset:
        labels_true = get_labels_from_list_of_tuple(labeled_sting)
        dev_string = get_dev_string_from_list_of_tuples(labeled_sting)
        parsed = parse(dev_string)
        labels_pred = [token[1] for token in parsed]
        hamming_loss += count_hamming_loss(labels_pred, labels_true, **kwargs)
        if labels_are_equal(labels_pred, labels_true, **kwargs):
            print(dev_string, "...ok")
        else:
            failed_critical += 1
            print("*" * 40)
            print(dev_string, "...INCORRECT PARSING")
            print("pred: ", labels_pred)
            print("true: ", labels_true)
            print("-" * 40)
        # if not labels_are_equal(labels_pred, labels_true, **kwargs):
        #     failed_critical += 1
        #     # print("*" * 40)
        #     # print(dev_string, "...INCORRECT PARSING")
        #     # print("pred: ", labels_pred)
        #     # print("true: ", labels_true)
        #     # print("-" * 40)

    print("Failed", failed_critical, "out of", dataset_length, "strings")
    print("Accuracy", (dataset_length - failed_critical) / float(dataset_length) * 100, "%")
    print("Hamming loss", hamming_loss / dataset_length)


def divide_on_ten_data_sets(data_set):
    divided_data_set = []
    for i in range(10):
        data_len = len(data_set)
        start_point = i * data_len / 10
        end_point = (i + 1) * data_len / 10
        divided_data_set.append(data_set[start_point:end_point])
    return divided_data_set


def launch():
    full_name_file = os.path.join(BASE_DIR, 'training/training_data/dev_labeled.xml')
    # full_name_file = os.path.join(BASE_DIR, 'training_data/full_labeled.xml')
    # full_name_file = os.path.join(BASE_DIR, '..', 'name_data/labeled/company_labeled.xml')
    # full_name_file = os.path.join(BASE_DIR, 'name_data/labeled/junk.xml')
    # full_name_file = os.path.join(BASE_DIR, 'mahara-full-names/labeled_xml/dev_set.xml')
    # full_name_file = os.path.join(BASE_DIR, 'mahara-full-names/labeled_xml/train_set.xml')
    critical_labels = ['GivenName', 'Surname', 'MiddleName', 'CorporationName']
    # critical_labels = None
    # full_name_file = os.path.join(BASE_DIR, 'training_data/full_labeled.xml')

    tree = ElementTree.parse(full_name_file)
    root = tree.getroot()
    xml_list_of_dicts = XmlListConfig(root)
    dev_set = []
    for dict_element in xml_list_of_dicts:
        dev_set.append(dict_element)
    # measure_accuracy(divide_on_ten_data_sets(dev_set)[0])
    # print(dev_set)
    measure_accuracy_given_surname(dev_set, critical_labels=critical_labels)
    # measure_accuracy_given_surname(dev_set)
    # for one_of_ten_part_of_data_set in divide_on_ten_data_sets(dev_set):
    #     measure_accuracy(one_of_ten_part_of_data_set)


if __name__ == '__main__':
    launch()

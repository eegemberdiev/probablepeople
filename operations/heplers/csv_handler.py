import csv


def read_matrix_from_csv(path_to_file, ignore_headers=False):
    with open(path_to_file) as csv_file:
        matrix = []
        reader = csv.reader(csv_file)
        if ignore_headers:
            next(reader)
        for row_string in reader:
            matrix.append(row_string)
        return matrix


def read_dict_from_csv(path_to_file):
    with open(path_to_file) as csv_file:
        matrix = []
        reader = csv.DictReader(csv_file)
        for row_string in reader:
            matrix.append(row_string)
        return matrix

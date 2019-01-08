from __future__ import print_function

import os
import random

from parserator import data_prep_utils

import probablepeople
from training_data_prep.census_names import makeTaggedData, makeInitialTaggedData

SURNAME_GIVEN_MIDDLE_LIMIT = 528560
SURNAME_GIVEN_MIDDLE_INITIAL_LIMIT = 292972
SURNAME_GIVEN_SUFFIX_LIMIT = 8934
SURNAME_GIVEN_MIDDLE_SUFFIX_LIMIT = 9388
SUFFIXES_GENERATIONAL = ['jr', 'JR', 'ii', 'II', 'iii', 'III', 'iv', 'IV']


def get_leader(leader, **kwargs):
    leading_names = dict(**kwargs).get(leader)
    if leading_names is None:
        raise ValueError(
            'Leader argument must be a sting name of one of %s' % dict(**kwargs).keys())


def expand_name(additional):
    return random.sample(additional, 1)


def get_random_tagged_token(tagged_tokens):
    return random.sample(tagged_tokens, 1)[0]


def get_random_suffix_generational_token(suffixes=None):
    if suffixes is None:
        suffixes = SUFFIXES_GENERATIONAL
    tagged_suffix = (random.sample(suffixes, 1)[0], 'SuffixGenerational')
    return tagged_suffix


def concat_names(given_names, surnames=None, middle_names=None):
    if not any([surnames, middle_names]):
        raise Exception('At least two lists must be provided')
    shuffled_names = []
    for first_name in given_names:
        full_name = [first_name]
        if surnames:
            full_name.extend(expand_name(surnames))
        if middle_names:
            full_name.extend(expand_name(middle_names))
        random.shuffle(full_name)
        shuffled_names.append(full_name)
    if surnames:
        for surname in surnames:
            full_name = [surname]
            full_name.extend(expand_name(given_names))
            if middle_names:
                full_name.extend(expand_name(middle_names))
            random.shuffle(full_name)
            shuffled_names.append(full_name)
    if middle_names:
        for middle_name in middle_names:
            full_name = [middle_name]
            full_name.extend(expand_name(given_names))
            if surnames:
                full_name.extend(expand_name(surnames))
            random.shuffle(full_name)
            shuffled_names.append(full_name)
    return shuffled_names


def form_sgm(given_names, surnames, middle_names, leader):
    leading_names = {'given_names': given_names,
                     'surnames': surnames,
                     'middle_names': middle_names
                     }.get(leader)
    if leading_names is None:
        raise ValueError('leader argument must be a sting name of one of ["given_names", "surnames", "middle_names"]')
    labeled_full_names = []

    for name in leading_names:
        full_name = [name]
        if surnames and leading_names is not surnames:
            full_name.insert(0, get_random_tagged_token(surnames))
        if given_names and leading_names is not given_names:
            full_name.insert(1, get_random_tagged_token(given_names))
        if middle_names and leading_names is not middle_names:
            full_name.insert(2, get_random_tagged_token(middle_names))
        labeled_full_names.append(full_name)
    return labeled_full_names


def form_sgmi(given_names, surnames, middle_initials, leader):
    leading_names = get_leader(leader, given_names=given_names, surnames=surnames, middle_initials=middle_initials)
    labeled_full_names = []

    for name in leading_names:
        full_name = [name]
        if surnames and leading_names is not surnames:
            full_name.insert(0, get_random_tagged_token(surnames))
        if given_names and leading_names is not given_names:
            full_name.insert(1, get_random_tagged_token(given_names))
        if middle_initials and leading_names is not middle_initials:
            full_name.insert(2, get_random_tagged_token(middle_initials))
        labeled_full_names.append(full_name)
    return labeled_full_names


def form_sgx(given_names, surnames, leader):
    leading_names = get_leader(leader, given_names=given_names, surnames=surnames)
    labeled_full_names = []

    for name in leading_names:
        full_name = [name]
        if surnames and leading_names is not surnames:
            full_name.insert(0, get_random_tagged_token(surnames))
        if given_names and leading_names is not given_names:
            full_name.insert(1, get_random_tagged_token(given_names))
        full_name.insert(2, get_random_suffix_generational_token())
        labeled_full_names.append(full_name)
    return labeled_full_names


def form_sgmx(given_names, surnames, middle_names, leader):
    leading_names = get_leader(leader, given_names=given_names, surnames=surnames, middle_names=middle_names)
    labeled_full_names = []

    for name in leading_names:
        full_name = [name]
        if surnames and leading_names is not surnames:
            full_name.insert(0, get_random_tagged_token(surnames))
        if given_names and leading_names is not given_names:
            full_name.insert(1, get_random_tagged_token(given_names))
        full_name.insert(2, get_random_suffix_generational_token())
        labeled_full_names.append(full_name)
    return labeled_full_names


def concat_names_by_sgm(given_names, surnames=None, middle_names=None, limit=SURNAME_GIVEN_MIDDLE_LIMIT):
    shuffled_names = form_sgm(given_names, surnames, middle_names, 'given_names')
    if surnames:
        shuffled_names.extend(form_sgm(given_names, surnames, middle_names, 'surnames'))
    if middle_names:
        shuffled_names.extend(form_sgm(given_names, surnames, middle_names, 'middle_names'))
    random.shuffle(shuffled_names)
    return shuffled_names[:limit]


def concat_names_by_sgmi(given_names, surnames, middle_initials, limit=SURNAME_GIVEN_MIDDLE_INITIAL_LIMIT):
    shuffled_names = form_sgmi(given_names, surnames, middle_initials, 'given_names')
    if surnames:
        shuffled_names.extend(form_sgmi(given_names, surnames, middle_initials, 'surnames'))
    if middle_initials:
        shuffled_names.extend(form_sgmi(given_names, surnames, middle_initials, 'middle_initials'))
    random.shuffle(shuffled_names)
    return shuffled_names[:limit]


def concat_names_by_sgx(given_names, surnames, limit=SURNAME_GIVEN_SUFFIX_LIMIT):
    shuffled_names = form_sgx(given_names, surnames, 'given_names')
    if surnames:
        shuffled_names.extend(form_sgx(given_names, surnames, 'surnames'))
    random.shuffle(shuffled_names)
    return shuffled_names[:limit]


def concat_names_by_sgmx(given_names, surnames, middle_names, limit=SURNAME_GIVEN_MIDDLE_SUFFIX_LIMIT):
    shuffled_names = form_sgmx(given_names, surnames, 'given_names')
    if surnames:
        shuffled_names.extend(form_sgmx(given_names, surnames, 'surnames'))
    if middle_names:
        shuffled_names.extend(form_sgmx(given_names, surnames, middle_names, 'middle_names'))
    random.shuffle(shuffled_names)
    return shuffled_names[:limit]


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    surname_file = os.path.join(BASE_DIR, 'training_data_prep/unlabeled_data/mahara_surnames.csv')
    female_given_file = os.path.join(BASE_DIR, 'training_data_prep/unlabeled_data/mahara_female.csv')
    female_middle_file = os.path.join(BASE_DIR, 'training_data_prep/unlabeled_data/mahara_middle_female.csv')
    male_given_file = os.path.join(BASE_DIR, 'training_data_prep/unlabeled_data/mahara_male.csv')
    male_middle_file = os.path.join(BASE_DIR, 'training_data_prep/unlabeled_data/mahara_middle_male.csv')

    surname_tagged = makeTaggedData(surname_file, 'Surname')
    male_given_tagged = makeTaggedData(male_given_file, 'GivenName')
    male_middle_tagged = makeTaggedData(male_given_file, 'MiddleName')
    male_middle_initial_tagged = makeInitialTaggedData(male_given_file, 'MiddleInitial')
    female_given_tagged = makeTaggedData(female_given_file, 'GivenName')
    female_middle_tagged = makeTaggedData(female_given_file, 'MiddleName')
    female_middle_initial_tagged = makeInitialTaggedData(female_given_file, 'MiddleInitial')

    # full_male_names = concat_names(male_given_tagged, surname_tagged, male_middle_tagged)
    # full_female_names = concat_names(female_given_tagged, surname_tagged, female_middle_tagged)

    full_names_without_comma = []
    # sgm_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # sgm_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_without_comma.extend(sgm_male_names + sgm_female_names)

    # sgmi_male_names = concat_names_by_sgmi(male_given_tagged, surname_tagged, male_middle_initial_tagged)
    # sgmi_female_names = concat_names_by_sgmi(female_given_tagged, surname_tagged, female_middle_initial_tagged)
    # full_names_without_comma.extend(sgmi_male_names + sgmi_female_names)

    # sgx_male_names = concat_names_by_sgx(male_given_tagged, surname_tagged)
    # full_names_without_comma.extend(sgx_male_names)

    sgmx_male_names = concat_names_by_sgmx(male_given_tagged, surname_tagged, male_middle_tagged)
    sgmx_female_names = concat_names_by_sgmx(female_given_tagged, surname_tagged, female_middle_tagged)
    full_names_without_comma.extend(sgmx_male_names + sgmx_female_names)
    #
    # sxgm_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # sxgm_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_without_comma.extend(sxgm_male_names + sxgm_female_names)
    #
    # sxgmi_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # sxgmi_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_without_comma.extend(sxgmi_male_names + sxgmi_female_names)
    #
    # sgmix_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # sgmix_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_without_comma.extend(sgmix_male_names + sgmix_female_names)
    #
    # sgimx_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # sgimx_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_without_comma.extend(sgimx_male_names + sgimx_female_names)
    #
    # sgimix_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # sgimix_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_without_comma.extend(sgimix_male_names + sgimix_female_names)

    # Comma containing tagged full names
    full_names_with_comma = []
    # s_comma_gm_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # s_comma_gm_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_with_comma.extend(s_comma_gm_male_names + s_comma_gm_female_names)
    #
    # s_comma_gmi_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # s_comma_gmi_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_with_comma.extend(s_comma_gmi_male_names + s_comma_gmi_female_names)
    #
    # s_comma_gx_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # s_comma_gx_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_with_comma.extend(s_comma_gx_male_names + s_comma_gx_female_names)
    #
    # s_comma_gmx_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # s_comma_gmx_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_with_comma.extend(s_comma_gmx_male_names + s_comma_gmx_female_names)
    #
    # s_comma_gmix_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # s_comma_gmix_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_with_comma.extend(s_comma_gmix_male_names + s_comma_gmix_female_names)
    #
    # s_comma_gimx_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # s_comma_gimx_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_with_comma.extend(s_comma_gimx_male_names + s_comma_gimx_female_names)
    #
    # s_comma_gimix_male_names = concat_names_by_sgm(male_given_tagged, surname_tagged, male_middle_tagged)
    # s_comma_gimix_female_names = concat_names_by_sgm(female_given_tagged, surname_tagged, female_middle_tagged)
    # full_names_with_comma.extend(s_comma_gimix_male_names + s_comma_gimix_female_names)

    full_names = full_names_with_comma + full_names_without_comma
    random.shuffle(full_names)

    thirty_percent = len(full_names) * 3 / 100
    dev_data_set = full_names[:thirty_percent]
    test_data_set = full_names[thirty_percent:]

    data_prep_utils.appendListToXMLfile(test_data_set, probablepeople,
                                        os.path.join(BASE_DIR, 'training/training_data/labeled.xml'))
    data_prep_utils.appendListToXMLfile(dev_data_set, probablepeople,
                                        os.path.join(BASE_DIR, 'training/training_data/dev_labeled.xml'))

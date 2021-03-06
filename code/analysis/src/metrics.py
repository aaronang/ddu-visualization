import csv
import math
import os
import re
from functools import reduce

from matrix import transpose, unique
from spectra import csv_to_spectra


def _spectra_to_dict(spectra):
    return {c[0]: c[1:] for c in spectra}


def _parent_dicts(parents):
    return {parent: {} for parent in parents}


def _density(activity):
    a = sum(activity, [])
    try:
        return sum(a) / len(a)
    except ZeroDivisionError:
        return 0


def normalized_density(activity):
    p = _density(activity)
    return 1 - math.fabs(1 - 2 * p)


def _remove_no_hit(transactions, transaction):
    test, hits = transaction
    if sum(hits) > 0:
        transactions += [transaction]
    return transactions


def diversity(activity):
    transactions = transpose(activity)
    unique_transactions = unique(transactions)
    buckets = list(map(lambda t: transactions.count(t), unique_transactions))
    numerator = reduce(lambda s, n: s + n * (n - 1), buckets, 0)
    num_of_transactions = len(transactions)
    denominator = num_of_transactions * (num_of_transactions - 1)
    try:
        return 1 - numerator / denominator
    except ZeroDivisionError:
        return 0


def uniqueness(activity):
    g = unique(activity)
    try:
        return len(g) / len(activity)
    except ZeroDivisionError:
        return 0


def _unit_and_integration(parent, transactions):
    def _is_unit(transaction):
        t, h = transaction
        return parent in t

    unit_tests = len(list(filter(_is_unit, transactions)))
    integration_tests = len(transactions) - unit_tests
    return unit_tests, integration_tests


def write_transactions(transactions, parent):
    current_dir = os.path.dirname(__file__)
    output_dir = os.path.join(current_dir, '../output/spectra/')
    output_file = os.path.join(output_dir, parent)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_file, 'w') as f:
        for t, h in transactions:
            print(h, t)
            f.write(str(h) + ' ' + t + '\n')


def compute_metrics(spectra, parents):
    transaction_names = transpose(spectra)[0][1:]
    spectra = transpose(spectra)[1:]
    spectra_dict = _spectra_to_dict(spectra)
    ddus = _parent_dicts(parents)
    for p, cs in parents.items():
        constructor = p + '#' + p.split('.')[-1]
        pattern = re.compile("%s\(.*\)" % constructor)
        components = list(filter(lambda c: pattern.match(c) is None, cs))
        components_activity = list(map(lambda c: spectra_dict[c], components))
        transactions = transpose(components_activity)
        transactions = zip(transaction_names, transactions)
        transactions = reduce(_remove_no_hit, transactions, [])
        print('\nParent:', p)
        print('Components:', components)
        if not transactions:
            continue
        if len(components) >= 8:
            write_transactions(transactions, p)
        ddus[p]['unit_tests'], ddus[p]['integration_tests'] = _unit_and_integration(p, transactions)
        tests, transactions = zip(*transactions)
        components_activity = transpose(transactions)
        ddus[p]['number_of_components'] = len(components)
        ddus[p]['number_of_tests'] = len(transactions)
        ddus[p]['density'] = _density(components_activity)
        ddus[p]['normalized_density'] = normalized_density(components_activity)
        ddus[p]['diversity'] = diversity(components_activity)
        ddus[p]['uniqueness'] = uniqueness(components_activity)
        # res = ddus[p]['normalized_density'] + ddus[p]['diversity'] + ddus[p]['uniqueness']
        # ddus[p]['ddu'] = res / 3.0 if res else 0
        ddus[p]['ddu'] = ddus[p]['normalized_density'] * ddus[p]['diversity'] * ddus[p]['uniqueness']
    return ddus


def _write_to_csv(csvname, ddus):
    dir = os.path.dirname(__file__)
    filename = os.path.normpath(os.path.join(dir, '../output/' + csvname))
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = [
            'parent',
            'number_of_components',
            'number_of_tests',
            'unit_tests',
            'integration_tests',
            'density',
            'normalized_density',
            'diversity',
            'uniqueness',
            'ddu']
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for parent, data in ddus.items():
            row = {'parent': parent}
            row.update(data)
            writer.writerow(row)


def metric_to_csv(csvname, granularity='method'):
    spectra, components = csv_to_spectra(csvname, granularity)
    metrics = compute_metrics(spectra, components)
    output_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '../output/' + granularity))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    _write_to_csv(granularity + '/' + csvname, metrics)


def metrics_to_csv(granularity='method'):
    dir = os.path.dirname(__file__)
    directory = os.path.normpath(os.path.join(dir, '../data/spectra/'))
    output_dir = os.path.normpath(os.path.join(dir, '../output/'))
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            print('Computing metrics for', directory + '/' + filename)
            metric_to_csv(filename, granularity)
            print(
                'Successfully written metrics to',
                output_dir + '/' + filename)

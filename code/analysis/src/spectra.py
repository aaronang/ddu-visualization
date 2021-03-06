import csv
import re
import os

from functools import reduce
from matrix import transpose, unique


def _get_class(name):
    return re.split(r'[#$]+', name)[0]


def _append(a, b):
    c = list(map(lambda x: _to_int(x), b))
    a.append(c)
    return a


def _to_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def _indexes(x, xs):
    return [i for (i, c) in enumerate(xs) if x == c]


def _flatten_spectra(spectra):
    components = spectra[0]
    transactions = spectra[1:]
    unique_components = set(components[1:])
    for component in unique_components:
        positions = _indexes(component, components)
        for j, transaction in enumerate(transactions):
            if sum([transaction[i] for i in positions]) > 0:
                for p in positions:
                    transactions[j][p] = 1
    data = [components] + transactions
    component_columns = transpose(data)
    return transpose(unique(component_columns))


def _is_test(x, y):
    if 'test' not in y[0] and 'Test' not in y[0]:
        x.append(y)
    return x


def _remove_tests(spectra):
    components = transpose(spectra)
    no_tests = reduce(_is_test, components, [])
    return transpose(no_tests)


def _unique_components(spectra):
    return set(spectra[0][1:])


def _get_package(name):
    return re.sub(r'\.[A-Z].*', '', name)


def _get_packages(spectra):
    components = _unique_components(spectra)
    packages = list(map(_get_package, components))
    packages = unique(packages)
    return reduce(_assign_package, components, _parent_dict(packages))


def _assign_package(packages, component):
    key = _get_package(component)
    keys = [k for k in packages if k in key]
    for k in keys:
        packages[k].append(component)
    return packages


def _parent_dict(parents):
    return {parent: [] for parent in parents}


def _get_classes(spectra):
    components = _unique_components(spectra)
    classes = unique(list(map(_get_class, components)))
    return reduce(_assign_class, components, _parent_dict(classes))


def _assign_class(classes, component):
    key = _get_class(component)
    keys = [k for k in classes if k in key]
    for k in keys:
        classes[k].append(component)
    return classes


def _get_method(name):
    return re.sub(r'\$\w*', '', name)


def _get_branch(name):
    return re.sub(r'\$\w*', '', name)


def _granularity(name='class'):
    granularities = {
        'branch': (_get_branch, _get_classes),
        'method': (_get_method, _get_classes),
        'method-package': (_get_method, _get_packages),
        'class': (_get_class, _get_packages)
    }
    return granularities[name]


def csv_to_spectra(input, granularity='method'):
    get_component, get_parent = _granularity(granularity)
    dir = os.path.dirname(__file__)
    filename = os.path.normpath(os.path.join(dir, '../data/spectra/' + input))
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        full_name_components = next(reader)
        components = list(map(get_component, full_name_components))
        activity = reduce(_append, reader, [])
        spectra = [components] + activity
        filtered = _remove_tests(_flatten_spectra(spectra))
        return filtered, get_parent(filtered)


"""REST API for available resources."""
import flask
import hirespy
from hirespy.api.error import InvalidUsage

import os


def preload():
    options = {}
    classification = ''
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'options.txt'), 'r') as lines:
        cnt = 0
        for line in lines:
            line = line.strip()
            if line in ['tissue', 'cell line', 'primary cell', 'in vitro differentiated cells']:
                classification = line
                options[classification] = {}
                continue
            term, donor = line.replace('_', ' '), 'mixed (default)'

            if classification in ['cell line', 'primary cell', 'in vitro differentiated cells']:
                donor = 'biosample donor (default)'
            if line[-4:-2] in ['_m', '_f']:
                term = term[:-4]
                if term == 'peyer s patch':
                    term = 'peyer\'s patch'
                if line[-3] == 'm':
                    if line[-2:] == '37':
                        donor = 'GTEX-1JKYN (male, 37yrs)'#'male, age {}'.format(line[-2:])
                    elif line[-2:] == '54':
                        donor = 'GTEX-1K2DA (male, 54yrs)'
                    else:
                        print(line)
                        exit(1)
                else:
                    if line[-2:] == '51':
                        donor = 'GTEX-1LVAN (female, 51yrs)'#donor = 'female, age {}'.format(line[-2:])
                    elif line[-2:] == '53':
                        donor = 'GTEX-1LGRB (female, 53yrs)'
                    else:
                        print(line)
                        exit(1)
            if term not in ['ascending aorta', 'body of pancreas']:
                options[classification][term] = options[classification].get(term, {})
                options[classification][term][donor] = cnt
            cnt += 1

    tissue_list = list(options['tissue'].keys())
    for tissue in tissue_list:
        new_name = '{} ({})'.format(tissue, len(options['tissue'][tissue]))
        options['tissue'][new_name] = options['tissue'][tissue].copy()
        del options['tissue'][tissue]

    return options

OPTIONS = preload()


@hirespy.app.route('/api/v1/options/terms/<classification>/', methods=["GET"])
def option_term(classification):
    """Return available resources."""
    if classification not in OPTIONS:
        return None
    context = {
        'terms': ['default']
    }
    context['terms'] = list(OPTIONS[classification].keys())

    return flask.jsonify(**context)


@hirespy.app.route('/api/v1/options/donors/<term>/', methods=["GET"])
def option_donor(term):
    """Return available resources."""
    classification, term = term.split('_')
    if classification not in OPTIONS:
        return None
    if term not in OPTIONS[classification]:
        return None
    context = {
        'donors': ['default']
    }
    context['donors'] = OPTIONS[classification][term]

    return flask.jsonify(**context)
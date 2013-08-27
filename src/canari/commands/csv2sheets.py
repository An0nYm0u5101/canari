#!/usr/bin/env python

from common import cmd_name

from argparse import ArgumentParser
from re import sub, match


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


parser = ArgumentParser(
    description='Convert mixed entity type CSVs to separated CSV sheets.',
    usage='canari %s <graph csv> <sheet prefix>' % cmd_name(__name__)
)

parser.add_argument(
    'graph',
    metavar='<graph csv>',
    help='The CSV file containing the output from the mtgx2csv command.'
)

parser.add_argument(
    'prefix',
    metavar='<sheet prefix>',
    help='The prefix to prepend to the generated CSV files.'
)


def help_():
    parser.print_help()


def description():
    return parser.description


def parse_args(args):
    return parser.parse_args(args)


def run(args):

    opts = parse_args(args)

    matchers = {}

    for line in file(opts.graph):
        line.replace('""', '&quot;')
        matcher = sub('=([^"]+)"', '=([^"]+)"', line)

        if matcher not in matchers:
            matchers[matcher] = []

        matchers[matcher].append(line)


    i = 0
    for matcher in matchers:
        f = open('%s_%d.csv' % (opts.prefix, i), 'w')
        i += 1

        f.write(matcher.replace('=([^"]+)', ''))

        for r in matchers[matcher]:
            line = '","'.join(match(matcher, r).groups())
            line = '"%s"\n' % line
            line.replace('&quot;', '""')
            f.write(line)

        f.close()

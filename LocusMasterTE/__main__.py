#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Main functionality of LocusMasterTE

"""
from __future__ import absolute_import

import sys
import os
import argparse
import errno

from ._version import VERSION
from . import LocusMasterTE_assign


__author__ = 'Sojung LEE, Matthew L. Bendall'
__copyright__ = "Copyright (C) 2023 Sojung LEE, Matthew L. Bendall"


USAGE   = ''' %(prog)s <command> [<args>]

The most commonly used commands are:
   assign    Reassign ambiguous fragments that map to repetitive elements
'''

def generate_test_command(args, seq_mode):
    try:
        _ = FileNotFoundError()
    except NameError:
        class FileNotFoundError(OSError):
            pass

    _base = os.path.dirname(os.path.abspath(__file__))
    _data_path = os.path.join(_base, 'data')
    _alnpath = os.path.join(_data_path, 'alignment.bam')
    _gtfpath = os.path.join(_data_path, 'annotation.gtf')
    if not os.path.exists(_alnpath):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), _alnpath
        )
    if not os.path.exists(_gtfpath):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), _gtfpath
        )
    print('LocusMasterTE %s assign %s %s' % (seq_mode, _alnpath, _gtfpath), file=sys.stdout)

def main():
    if len(sys.argv) == 1:
        empty_parser = argparse.ArgumentParser(
            description='Tools for analysis of repetitive DNA elements',
            usage=USAGE,
        )
        empty_parser.print_help(sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Tools for analysis of repetitive DNA elements',
    )
    parser.add_argument('--version',
        action='version',
        version=VERSION,
        default=VERSION,
    )

    subparsers = parser.add_subparsers(help='Sequencing modality help', dest = 'bulk')

    ''' Parser for bulk RNA-seq '''
    bulk_parser = subparsers.add_parser('bulk',
        description='''LocusMasterTE for bulk RNA-sequencing data sets''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    bulk_subparser = bulk_parser.add_subparsers(help='Bulk RNA-seq sub-command help', dest='subcommand')

    ''' Parser for bulk RNA-seq assign '''
    bulk_assign_parser = bulk_subparser.add_parser('assign',
        description='''Reassign ambiguous fragments that map to repetitive elements (bulk RNA-seq)''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    LocusMasterTE_assign.BulkIDOptions.add_arguments(bulk_assign_parser)
    bulk_assign_parser.set_defaults(func=lambda args: LocusMasterTE_assign.run(args))

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

#!python

from importlib import import_module
from argparse import ArgumentParser, RawTextHelpFormatter
from textwrap import dedent
from idgrms.data import *
from idgrms.plotdgrms import *


argparser = ArgumentParser(
    prog='interactive_diagrams.py',
    description='>> Display and interact with diagrams <<',
    epilog='Copyright (c) 2019 Przemysław Bruś',
    formatter_class=RawTextHelpFormatter
)
argparser.add_argument(
    'data_file',
    help=dedent('''\
    The name of a file which must contain columns with data:
    id value_1 value_2 value_3 ...
    ------------------------------
    int float float float ...

    Only the first column must be an integer, the rest must
    be float. Additionally, the file must contain a one-line
    header. The header must be preceded by # sign. Labels from
    the header are used to mark axes on diagrams.
    ''')
)
argparser.add_argument(
    '--col',
    help=dedent('''\
    The columns numbers which will be used to create diagrams.

    A negative number reverses an axis range. There is no limit
    of a diagrams amount, just add another --col arguments.
    '''),
    nargs=2,
    dest='columns',
    action='append',
    metavar=('x', 'y'),
    required=True,
    type=int
)
argparser.add_argument(
    '--grp',
    help=dedent('''\
    Group of stars which can be marked by [color].

    [file] should contain only one column with ID numbers. If this
    option is used, [data_file] must have the same ID numbers in
    the first column.

    The [color] marks points from [file]. The color can be specified
    by an html hex string ("#4f21b7") or literally (blue or b).
    '''),
    nargs=2,
    dest='grp',
    action='append',
    metavar=('file', 'color')
)
argparser.add_argument(
    '-t',
    help=dedent('''\
    Talkative mode. Print feedback with every click.
    '''),
    action='store_true'
)
argparser.add_argument(
    '-v',
    '--version',
    action='version',
    version=dedent('''\
    %(prog)s
    * Version: ''' + import_module('idgrms').__version__ + '''
    * Licensed under the MIT license:
    * http://opensource.org/licenses/MIT
    * ''' + argparser.epilog)
)

args = argparser.parse_args()
trigger_windows(args.data_file, args.columns, args.grp, args.t)

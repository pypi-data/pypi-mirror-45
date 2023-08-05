import argparse

from .find import find, find_list 
from .tree_search import TreeSearch

if __name__ == '__main__':
    parser = argparser.ArgumentParser(
        description='Place description here.')

    parser.add_argument('root', default='.', metavar='root', dest='root',
        help='A helpful message.')
    parser.add_argument('-type', default='*', metavar='file_type',
        dest='file_type', help='A helpful message.')
    parser.add_argument('-name', default=None, metavar='name', dest='name',
        help='A helpful message.')

    args = parser.parse_args()
    find(args.root, args.name, args.file_type)

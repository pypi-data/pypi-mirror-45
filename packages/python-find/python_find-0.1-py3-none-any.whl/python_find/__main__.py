import argparse

from .find import find

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='python_find',
        description='Place description here.')

    parser.add_argument('root', nargs='?', default='.', metavar='root',
        help='Directory to root search.')
    parser.add_argument('-type', default='*', metavar='file_type',
        dest='file_type', choices=['d', 'f', 'l'],
        help='Type of files to consider in search.')
    parser.add_argument('-name', default=None, metavar='name',
        help='Regex expression used to search.')

    args = parser.parse_args()

    try:
        find(args.root, args.name, args.file_type)

    except KeyboardInterrupt:
        pass

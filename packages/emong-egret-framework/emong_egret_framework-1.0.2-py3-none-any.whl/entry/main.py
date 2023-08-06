import argparse
from entry.args.create import *
from entry.args.platform import *

def main():
    # example.main()
    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers()

    sub_init = sub.add_parser('create')
    sub_init.add_argument('--name', required=True, help='project name')
    sub_init.set_defaults(func=create)

    sub_platform = sub.add_parser('platform')
    sub_platform.add_argument('--name', choices=['kakao', 'facebook', 'line', 'playgg', 'gstar'])
    sub_platform.set_defaults(func=platform)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)


if __name__ == '__main__':
    main()

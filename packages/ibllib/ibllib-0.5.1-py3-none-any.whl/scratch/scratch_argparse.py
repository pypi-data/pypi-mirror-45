# -*- coding:utf-8 -*-
# @Author: Niccolò Bonacchi
# @Date: Tuesday, March 26th 2019, 3:00:11 pm
# @Last Modified by: Niccolò Bonacchi
# @Last Modified time: 26-03-2019 03:01:48.4848
"""
Usage:
    update.py
        Will fetch changes from origin and update iblrig and lib to latest
        revision on master
    update.py -v <version>
        Will checkout the <version> release and import task files to pybpod.
    update.py -b <branch>
        Will checkout the latest commit of <branch> and import task files to
        pybpod.
    update.py --info
        Will display information on versions and branches.
    update.py --reinstall
        Will reinstall the rig to the latest revision on master.
    update.py --ibllib
        Will reset ibllib to latest revision on master and install to iblenv.
    update.py --update
        Will update itself to the latest revision on master.
    update.py --update -b <branch>
        Will update itself to the latest revision on <branch>.
"""
import argparse


def main(args):
    nargs_passed = sum([True for x in args.__dict__.values() if x])

    if not any(args.__dict__.values()):
        print('update_to_latest()')

    if nargs_passed == 2:
        if args.update and args.b:
            if args.b not in AVAILABLE_BRANCHES:
                print('Not found:', args.b)
                return
            print("checkout_single_file(file='update.py', branch=args.b)")
        else:
            print(NotImplemented)
        return
    elif nargs_passed == 1:
        if args.b and args.b in AVAILABLE_BRANCHES:
            print(AVAILABLE_BRANCHES,
                """checkout_branch(sys.argv[1])
                import_tasks()
                update_ibllib() """)
        elif args.b and args.b not in AVAILABLE_BRANCHES:
            print('Branch', args.b, 'not found')

        if args.update:
            print("checkout_single_file(file='update.py', branch='master')")

        if args.v and args.v in AVAILABLE_VERSIONS:
            print(AVAILABLE_VERSIONS,
                """checkout_version(sys.argv[1])
                import_tasks()
                update_ibllib() """)
        elif args.v and args.v not in AVAILABLE_VERSIONS:
            print('Version', args.v, 'not found')

        if args.reinstall:
            print('os.system("conda deactivate && python install.py")')

        if args.ibllib:
            print("update_ibllib()")

        if args.info:
            print('info()')

        return


if __name__ == "__main__":
    from pathlib import Path
    FILE = Path(__file__)
    print(FILE)
    print(Path().cwd())
    AVAILABLE_VERSIONS = ['1.0.0', '1.1.1']  # get_versions()
    AVAILABLE_BRANCHES = ['master', 'develop']  # get_branches()
    parser = argparse.ArgumentParser(description='Install iblrig')
    parser.add_argument('-v', required=False, default=False,
                        help='Available versions: ' + str(AVAILABLE_VERSIONS))
    parser.add_argument('-b', required=False, default=False,
                        help='Available branches: ' + str(AVAILABLE_BRANCHES))
    parser.add_argument('--reinstall', required=False, default=False,
                        action='store_true', help='Reinstall iblrig')
    parser.add_argument('--ibllib', required=False, default=False,
                        action='store_true', help='Update ibllib only')
    parser.add_argument('--update', required=False, default=False,
                        action='store_true', help='Update self: update.py')
    parser.add_argument('--info', required=False, default=False,
                        action='store_true',
                        help='Disply information on branches and versions')
    args = parser.parse_args()
    main(args)
    print('\n')

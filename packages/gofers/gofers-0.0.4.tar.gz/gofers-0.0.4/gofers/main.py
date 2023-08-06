# encoding: utf-8
import os
from .loader import Generator
from .util import ConfigHandler


def cmd():
    import argparse
    parser = argparse.ArgumentParser(
        description='API test idea by commandline.',
        epilog='That\'s all about gofers usage description.')
    parser.add_argument('-v',
                        dest='version',
                        action='store_true',
                        help="show version")
    parser.add_argument('--project', dest='project', help="project path")
    parser.add_argument('--suite', dest='suite', help="testcase path")
    parser.add_argument('--startproject', help="Specify new project name.")

    args = parser.parse_args()

    if args.startproject:
        # TODO: create new project
        exit(0)

    if args.suite:
        try:
            Generator.scripts(args.suite)
            os.chdir(args.suite)
            config = ConfigHandler(args.suite)
            os.system(config.CMD_EXEC)
            os.chdir(config.REPORT_DIR)
            os.system(config.CMD_REPORT)
        except Exception:
            raise

    return 0

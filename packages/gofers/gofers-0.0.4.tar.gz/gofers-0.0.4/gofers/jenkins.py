import os

from gofers.factory import Generator, SCRIPT_DIR

Generator.scripts()
os.chdir(SCRIPT_DIR)

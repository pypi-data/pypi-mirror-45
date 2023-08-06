import os

from gofers.factory import Generator, SCRIPT_DIR, CMD_EXEC_PYTEST_ALLURE, REPORT_DIR, CMD_EXEC_PYTEST_ALLURE_GENERATE


def runner():
    Generator.scripts()
    os.chdir(SCRIPT_DIR)
    os.system(CMD_EXEC_PYTEST_ALLURE)
    os.chdir(REPORT_DIR)
    os.system(CMD_EXEC_PYTEST_ALLURE_GENERATE)


if __name__ == '__main__':
    runner()

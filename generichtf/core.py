from os import listdir
from os.path import isdir, join


class TestInstance:
    pass


class TestSuite:
    def __init__(self, root_dir: str):
        dir_list = [dir_name for dir_name in listdir(root_dir) if isdir(join(root_dir, dir_name))]

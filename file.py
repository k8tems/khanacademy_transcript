import os


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def read_text(fname):
    with open(fname) as f:
        return f.read()


def write_text(fname, text):
    with open(fname, 'w') as f:
        f.write(text)
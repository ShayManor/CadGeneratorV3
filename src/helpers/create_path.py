import os


def create_path(name: str):
    prefix = 'src/data'
    if not os.path.exists(os.path.join(prefix, name)):
        return os.path.join(prefix, name)
    index = 1
    while os.path.exists(os.path.join(prefix, name + str(index))):
        index += 1
    return os.path.join(prefix, name + str(index))

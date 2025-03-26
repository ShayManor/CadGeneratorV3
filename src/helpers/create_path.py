import os


def create_path(name: str):
    prefix = 'src/data'
    if not os.path.exists(os.path.join(prefix, name)):
        return os.path.join(prefix, name)
    index = 1
    while os.path.exists(os.path.join(prefix, name + str(index))):
        index += 1
    return os.path.join(prefix, name + str(index))


def get_image_name(name: str):
    return os.path.join('src/data', name)


def get_final_image_path(name: str):
    return create_path(name + 'final_image')

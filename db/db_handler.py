import pickle
import os
from conf import setting


def save(obj):
    path_obj = os.path.join(setting.BASE_DB, obj.__class__.__name__.lower())
    if not os.path.exists(path_obj):
        os.mkdir(path_obj)
    path_file = os.path.join(path_obj, obj.name)
    with open(path_file, 'wb') as f:
        pickle.dump(obj, f)
        f.flush()


def select(name, type):
    path_file = os.path.join(setting.BASE_DB,type, name)
    if  os.path.exists(path_file):
        with open(path_file, 'rb') as f:
            return pickle.load(f)
    else:
        return False

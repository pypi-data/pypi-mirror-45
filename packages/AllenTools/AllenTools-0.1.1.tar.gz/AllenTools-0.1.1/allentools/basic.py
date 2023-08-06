from functools import wraps
import os

def decode_bytes(b_str, encoding='utf-8'):
    if isinstance(b_str, str):
        return b_str
    return b_str.decode(encoding)

def exception_handler(func, abort=False):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            if abort:
                raise e
    return wrapper

def exist_file_ignore_extension(path, name):
    files = os.listdir(path)
    for i in files:
        if name == i.rsplit('.', 1)[0]:
            return True
    return False

def filename_ignore_extension(path, name, abs=False):
    files = os.listdir(path)
    for i in files:
        if name == i.rsplit('.', 1)[0]:
            return i if not abs else os.path.join(path, i)
    raise FileNotFoundError()
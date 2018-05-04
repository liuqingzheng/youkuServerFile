import hashlib
import time
import os
import time

def get_uuid(name):
    md = hashlib.md5()
    md.update(name.encode('utf-8'))
    md.update(str(time.clock()).encode('utf-8'))
    return md.hexdigest()


def get_all_file(file_dir):
    '''
    获得一个文件下所有文件的名字
    ps:
    os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表
    :param file_dir:
    :return:
    '''
    file_list = os.listdir(file_dir)
    return file_list


def get_time():
    now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return now_time
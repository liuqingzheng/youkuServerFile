from interface import login_user_data
from lib import common
from db import models


def login(user_dic, mutex):
    user = models.User.get_obj_by_name(user_dic['name'])
    if user:  # 用户存在
        if user.user_type == user_dic['user_type']:
            if user.password == user_dic['password']:
                session = common.get_uuid(user_dic['name'])
                mutex.acquire()
                login_user_data.alive_user[user_dic['addr']] = [session, user_dic['name']]
                mutex.release()
                back_dic = {'flag': True, 'session': session, 'msg': 'login success','is_vip':user.is_vip}
            else:
                back_dic = {'flag': False, 'msg': 'password error'}
        else:
            back_dic = {'flag': False, 'msg': '登录类型不匹配'}
    else:
        back_dic = {'flag': False, 'msg': 'user do not exisit'}
    return back_dic


def register(user_dic):
    user = models.User.get_obj_by_name(user_dic['name'])
    if user:  # 用户存在
        back_dic = {'flag': False, 'msg': 'user is exisit'}
    else:
        user = models.User(user_dic['name'], user_dic['password'], user_dic['user_type'])
        user.save()
        back_dic = {'flag': True, 'msg': 'register success'}

    return back_dic

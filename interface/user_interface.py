# 注册（用手机号注册，密码用md5加密）
# 登录（登录后显示最新一条公告）
# 冲会员
# 查看视频（即将所有视频循环打印出来）
# 下载普通视频（非会员下载视频需要等30s广告，会员下载无需等待）
# 下载收费视频（非会员下载需要10元，会员下载需要5元）
# 查看观影记录（就是查看自己下载过的视频）
# 查看公告（包括历史公告）
from db import models
import os
from conf import setting
from lib import common
import struct
import json


def buy_member(user_dic):
    user = models.User.get_obj_by_name(user_dic['name'])
    user.buy_member()
    user.save()
    back_dic = {'flag': True, 'msg': 'buy success'}
    return back_dic


def get_movie_list(user_dic):
    movie_list = common.get_all_file(setting.BASE_MOVIE_LIST)
    back_movie_list = []
    if movie_list:  # 不为空，继续查询，为空直接返回false
        for m in movie_list:
            movie = models.Movie.get_obj_by_name(m)
            if not movie.is_delete:
                back_movie_list.append([movie.name, '免费' if movie.is_free else '收费'])
        if back_movie_list:
            return {'flag': True, 'movie_list': back_movie_list}
        else:
            return {'flag': False, 'msg': '暂无可删除影片'}
    else:
        return {'flag': False, 'msg': '暂无影片'}


def download_movie(user_dic):
    movie = models.Movie.get_obj_by_name(user_dic['movie_name'])
    if not movie:  # 电影不存在，返回false
        back_dic = {'flag': False, 'msg': '该电影不存在'}
        return back_dic
    if user_dic['movie_type'] == 'free':  # 要下载免费视频
        if not movie.is_free:
            back_dic = {'flag': False, 'msg': '该电影为收费电影，请到收费区下载'}
            return back_dic
    elif user_dic['movie_type'] == 'charge':  # 要下载免费视频
        if movie.is_free:
            back_dic = {'flag': False, 'msg': '该电影为免费电影，请到免费区下载'}
            return back_dic

    user = models.User.get_obj_by_name(user_dic['name'])
    send_back_dic = {'flag': True}
    if user.is_vip:
        send_back_dic['wait_time'] = 0
    else:
        send_back_dic['wait_time'] = 30
    send_back_dic['filename'] = movie.name
    send_back_dic['filesize'] = os.path.getsize(movie.path)
    send_back_dic['path'] = movie.path
    user.add_download_record(movie.name)
    return send_back_dic


def check_notice(user_dic):
    path = os.path.join(setting.BASE_DB, 'notice')
    if not os.path.exists(path):
        return {'flag': False, 'msg': '暂无公告'}
    notice_list = common.get_all_file(path)
    back_notice_list = []
    if notice_list:  # 不为空，继续查询，为空直接返回false
        for m in notice_list:
            notice = models.Notice.get_obj_by_name(m)
            back_notice_list.append({notice.name: notice.content})
        return {'flag': True, 'notice_list': back_notice_list}
    else:
        return {'flag': False, 'msg': '暂无公告'}


def check_download_record(user_dic):
    user = models.User.get_obj_by_name(user_dic['name'])
    download_list = user.check_download_record()
    if download_list:
        back_dic = {'flag': True, 'msg': 'buy success', 'download_list': download_list}
        return back_dic
    else:
        back_dic = {'flag': False, 'msg': '暂无观影记录'}
        return back_dic


def send_back_method(back_dic, conn):
    head_json_bytes = json.dumps(back_dic).encode('utf-8')
    conn.send(struct.pack('i', len(head_json_bytes)))  # 先发报头的长度
    conn.send(head_json_bytes)

from conf import setting
import os
from db import models
from lib import common


def upload_movie(user_dic, conn):
    recv_size = 0
    print('----->', user_dic['file_name'])
    path = os.path.join(setting.BASE_MOVIE_LIST, user_dic['file_name'])
    with open(path, 'wb') as f:
        while recv_size < user_dic['file_size']:
            recv_data = conn.recv(1024)
            f.write(recv_data)
            recv_size += len(recv_data)
            # print('recvsize:%s filesize:%s' % (recv_size, user_dic['file_size']))
    print('%s :上传成功' % user_dic['file_name'])
    movie = models.Movie(user_dic['file_name'], path, user_dic['is_free'], user_dic['name'])
    movie.save()
    back_dic = {'flag': True, 'msg': '上传成功'}
    return back_dic


def delete_movie(user_dic):
    movie = models.Movie.get_obj_by_name(user_dic['movie_name'])
    movie.is_delete = 1   #1为删除，0为不删除
    movie.save()
    back_dic = {'flag': True, 'msg': '电影：%s 删除成功'%user_dic['movie_name']}
    return back_dic


def release_notice(user_dic):
    notice = models.Notice(user_dic['notice_name'], user_dic['notice_content'], user_dic['name'],common.get_time())
    notice.save()
    back_dic = {'flag': True, 'msg': '发布公告成功'}
    return back_dic
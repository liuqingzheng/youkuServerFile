import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from threading import current_thread, Thread
from conf import setting
import struct
import json
from interface import common_interface, admin_interface, user_interface, login_user_data
import time

server_pool = ThreadPoolExecutor(2)
mutex = Lock()
dispatch_dic = {
    'register': common_interface.register,
    'delete_movie': admin_interface.delete_movie,
    'release_notice': admin_interface.release_notice,
    'buy_member': user_interface.buy_member,
    'get_movie_list': user_interface.get_movie_list,
    'check_notice': user_interface.check_notice,
    'check_download_record': user_interface.check_download_record
}


def working(conn, addr):
    print(current_thread().getName())
    while True:
        try:
            head_struct = conn.recv(4)
            if not head_struct: break
            head_len = struct.unpack('i', head_struct)[0]
            head_json = conn.recv(head_len).decode('utf-8')
            head_dic = json.loads(head_json)

            head_dic['addr'] = addr[1]
            dispatch(head_dic, conn)
        except Exception:

            conn.close()
            # 把服务器保存的用户信息清掉
            mutex.acquire()
            if addr[1] in login_user_data.alive_user:
                login_user_data.alive_user.pop(addr[1])
            # print('***********end*************%s'%len(login_user_data.alive_user))
            mutex.release()

            print('客户端：%s :断开链接' % str(addr))

            break


def dispatch(head_dic, conn):

    if head_dic['type'] == 'login':  # 登录
        back_dic = common_interface.login(head_dic, mutex)
        send_back(back_dic, conn)
    elif head_dic['type'] == 'download_movie':  # 下载
        back_dic=user_interface.download_movie(head_dic)
        send_back(back_dic, conn)
        with open(back_dic['path'], 'rb')as f:
            for line in f:
                conn.send(line)

    elif head_dic['type'] == 'upload':  # 上传
        back_dic = admin_interface.upload_movie(head_dic, conn)
        send_back(back_dic, conn)
    else:
        if head_dic['type'] not in dispatch_dic:
            back_dic = {'flag': False, 'msg': '请求不存在'}
            send_back(back_dic, conn)
        else:
            back_dic = dispatch_dic[head_dic['type']](head_dic)
            send_back(back_dic, conn)
    #
    #
    # if head_dic['type'] == 'register':#注册
    #     back_dic = common_interface.register(head_dic)
    #     send_back(back_dic)
    # elif head_dic['type'] == 'login':#登录
    #     back_dic = common_interface.login(head_dic)
    #     send_back(back_dic, conn)
    # elif head_dic['type'] == 'upload':#上传视频
    #     admin_interface.upload_movie()
    # elif head_dic['type'] == 'delete_movie':#删除视频
    #     pass
    # elif head_dic['type'] == 'release_notice':#发布公告
    #     pass
    # elif head_dic['type'] == 'buy_member':#冲会员
    #     pass
    # elif head_dic['type'] == 'get_movie_list':  # 查看视频列表
    #     pass
    # elif head_dic['type'] == 'download':#下载视频
    #     user_interface.download_movie()
    #
    #
    # else:
    #     raise Exception('请求不存在')


def send_back(back_dic, conn):
    head_json_bytes = json.dumps(back_dic).encode('utf-8')
    conn.send(struct.pack('i', len(head_json_bytes)))  # 先发报头的长度
    conn.send(head_json_bytes)


def server_run():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(setting.server_address)
    socket_server.listen(5)

    while True:
        conn, addr = socket_server.accept()
        print('客户端:%s 链接成功' % str(addr))
        server_pool.submit(working, conn, addr)

        # t=Thread(target=communicate,args=(conn,addr,mutex))
        # t.start()
        # print('%sendendendend'%len(login_user_data.alive_user))
        # print(login_user_data.alive_user)

    socket_server.close()

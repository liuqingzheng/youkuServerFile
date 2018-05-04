from db import db_handler


class BaseClass:
    '''
    所有类的基类
    '''

    @classmethod
    def get_obj_by_name(cls, name):
        return db_handler.select(name, cls.__name__.lower())

    def save(self):
        db_handler.save(self)


class User(BaseClass):
    def __init__(self, name, password, user_type='user'):
        self.name = name
        self.password = password
        self.user_type = user_type
        self.is_vip = 0  # 0是非会员，1是会员，默认非会员
        self.download_list = []

    def upload_movie(self, movie_name, path, is_free):
        Movie(movie_name, path, is_free, self.name)

    def buy_member(self):
        self.is_vip = 1

    def add_download_record(self, movie_name):
        self.download_list.append(movie_name)
        self.save()

    def check_download_record(self):
        return self.download_list


class Movie(BaseClass):
    def __init__(self, name, path, is_free, owner):
        self.name = name
        self.path = path
        self.is_free = is_free
        self.owner = owner
        self.is_delete = 0

    def delete_movie(self):
        self.is_delete = 1


class Notice(BaseClass):
    def __init__(self, name, content, owner, create_time):
        self.name = name
        self.content = content
        self.owner = owner
        self.create_time = create_time

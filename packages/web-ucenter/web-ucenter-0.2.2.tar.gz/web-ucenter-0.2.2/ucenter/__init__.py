# coding=utf-8

from ucenter.db import mongo
from ucenter import routes


def init(app, load_routes=True):

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    if load_routes:
        app.load_routes(routes)

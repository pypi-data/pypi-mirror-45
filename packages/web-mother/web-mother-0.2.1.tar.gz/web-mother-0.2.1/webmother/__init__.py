# coding=utf-8

import ucenter
from .db import mongo
from . import routes
from .extra_passport import append_extra


def init(app):
    # 初始化UCenter
    ucenter.init(app)

    # 初始化本系统数据库
    mongo.init()

    # 增加本系统增加的权限需求
    append_extra()

    # 加载路由模块
    app.load_routes(routes)

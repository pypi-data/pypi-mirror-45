#!/usr/bin/python
# coding:utf-8

from config import MongoServer
import pymongo
from tornado.options import options
from sshtunnel import SSHTunnelForwarder

MongoCfg = {
    'authSource': 'ucdb',
    'username': 'app',
    'password': 'Uc2app',
    'connecttimeoutms': 60 * 1000
}

mongo_client = None
mongo_db = None

users = None


def init():
    if not MongoServer['active']:
        return

    global mongo_client
    global mongo_db
    global users

    if mongo_client is not None:
        return

    mongo_cfg = MongoServer[options.env]

    server = mongo_cfg['mongodb'].split(':')
    host = server[0]
    port = int(server[1]) if len(server) > 1 else 27017

    # 如果设置ssh登录，则通过ssh隧道登录（一般远程测试用）
    if 'ssh'in mongo_cfg and len(mongo_cfg['ssh']['pwd']) > 0:
        ssh_server = SSHTunnelForwarder(
            ssh_address_or_host=mongo_cfg['ssh']['address'],
            ssh_password=mongo_cfg['ssh']['pwd'],
            ssh_username=mongo_cfg['ssh']['usr'],
            remote_bind_address=(host, port))

        ssh_server.start()

        host = ssh_server.local_bind_host
        port = ssh_server.local_bind_port
    # END

    mongo_client = pymongo.MongoClient(host=host, port=port, **MongoCfg)
    mongo_db = mongo_client[MongoCfg['authSource']]

    # collections
    users = mongo_db.users

    # 创建索引
    _users_index()


def start_session():
    return mongo_client.start_session()


def _users_index():
    """ users sample
    {
        "_id": ObjectId("5c393f37e155ac54355b37ef"), # 用户ID，使用ObjectId
        "status": 1,                                 # 0: 锁定，1: 正常
        "name": "jack",                              # 登录帐号
        "email": "jack@qq.com",
        "mobile": "86-13012345678",                  # 格式："国家代码-号码"
        "card_id": "422420199009101234",
        "real_name": "张杰克",
        "nickname": "笨笨哥",
        "gender": 1,                                 # 1：男， 2：女
        "country_code": 86,
        "country": "中国",
        "province": "广东",
        "city": "深圳",
        "icon": "http://example.com/icon/jack.png",
        "birthday": "1990-09-10",
        "pwd_hash": "adsfas293rjlsdjfl232489",
        "salt": "23jkas2342",
        "created": 1546763523000,                    # 毫秒
        "updated": 1546763523000,                    # 毫秒
        "weixin": {
            "open_id": "a7823c872348d234889234d323",
            "union_id": "b34d2342a23423bb342c23dd",
            "nickname": "哈哈BBG",
            "icon": "http://qq.com/icon/jack.png",
            "extend": "any string"
        },
        "weibo": {
            "open_id": "cbd232d2342a23423f234e2342b",
            "union_id": "aadd898c899e98998e9e9bb8234",
            "nickname": "大杰张",
            "icon": "http://weibo.com/icon/jack.png",
            "extend": "any string"
        },
        "addresses": [
            {
                "receiver": "张杰克",
                "address": "深圳南山科技园路123号",
                "country_code": 86,
                "zip_code": 518000,
                "tel": "0755-26261234",
                "mobile": "86-13012345678",
                "is_default": 1
            }
        ]
    }
    """
    users.create_index('name', unique=True, sparse=True)
    users.create_index('email', unique=True, sparse=True)
    users.create_index('mobile', unique=True, sparse=True)
    users.create_index('card_id', unique=True, sparse=True)
    users.create_index('weixin.open_id', unique=True, sparse=True)
    users.create_index('weixin.union_id')
    users.create_index('wxmp.open_id', unique=True, sparse=True)
    users.create_index('wxmp.union_id')

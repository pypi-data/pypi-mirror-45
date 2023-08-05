# coding:utf-8

import config
import pymongo
from tornado.options import options
from webmother.db import mongo as mother_db

MongoDB = {
    'active': True,  # 是否启用
    'dev': {
        'host': config.Mongo['host'],
        'port': config.Mongo['port'],
        'db': 'proddb',
        'user': 'app',
        'pwd': 'Prod2app',
        'connecttimeoutms': 60 * 1000
    },
    'prod': {
        'host': config.Mongo['host'],
        'port': config.Mongo['port'],
        'db': 'proddb',
        'user': 'app',
        'pwd': 'Prod2app',
        'connecttimeoutms': 60 * 1000
    }
}

# web-mother相关集合
catalog = None
org = None
org2user = None
catalog2org = None

# product DB
mongo_client = None
mongo_db = None

product = None


def init():
    if not MongoDB['active']:
        return

    global catalog
    global org

    global org2user
    global catalog2org

    global mongo_client
    global mongo_db

    global product

    mongo_cfg = MongoDB[options.env]

    if mongo_client is not None:
        return

    mother_db.init()

    # 引用webmother中的数据集合
    catalog = mother_db.catalog
    org = mother_db.org
    org2user = mother_db.org2user
    catalog2org = mother_db.catalog2org
    # END

    mongo_client = pymongo.MongoClient(host=mongo_cfg['host'],
                                       port=mongo_cfg['port'],
                                       username=mongo_cfg['user'],
                                       password=mongo_cfg['pwd'],
                                       authSource=mongo_cfg['db'])
    mongo_db = mongo_client[mongo_cfg['db']]

    # my collections
    product = mongo_db.product
    # END

    # 创建索引
    _product_index()

    # 初始化系统数据
    _init_data()


def start_session():
    return mongo_client.start_session()


def _product_index():
    """
    {
        "_id": ObjectId('5c729df2e155ac16da86a1d0'),
        "name": "live-pledge",                           # 产品标示名，英文、数字、"-"
        "catalog": ObjectId('5c710622e155ac0c39c8b66d'), # 所属分类节点ID
        "status": 30,                                    # 状态：-10:已删除；0:编辑中；10:待审；20:休眠中；30:已激活；
        "display": {
            "zh": "活期质押",
            "en": "Live Pledge"
        },
        "desc": {
            "zh": "灵活的质押和支取",
            "en": "Pledge and draw flexibly"
        },
        "icon": "http://your.com/icon/pledge.png",
        "the_pledged": {...},   # 被质押的东西
        "the_loaned": {...},    # 被贷出的东西
        "normal_rate": 1.5,   # 正常质押率，质押率：质押资产市值/贷款货币市值
        "warn_rate": 1.1,     # 禁戒质押率
        "bomb_rate": 1.05,    # 爆仓质押率
        "interest_rate": 0.0001 # 贷款利率（日利率）
        "created": 1551015331186,
        "updated": 1551015331186
    }
    """
    product.create_index('name')
    product.create_index([('catalog', pymongo.ASCENDING), ("updated", pymongo.ASCENDING)], sparse=True)


def _init_data():
    pass

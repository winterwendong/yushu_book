# -*- coding:utf-8 -*-
__author__ = 'wendong'
__data__ = '2019-05-11 2:06'


DEBUG = True
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3308/yushu"

SECRET_KEY = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'

# Email 配置
MAIL_SERVER = 'smtp.sina.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'chwdeng@sina.com'
MAIL_PASSWORD = ''
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '鱼书 <hello@yushu.im>'
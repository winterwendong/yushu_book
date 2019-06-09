# -*- coding:utf-8 -*-
from flask import current_app

__author__ = 'wendong'
from app.spider.yushu_book import YushuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc,func
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from collections import namedtuple


EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])

class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
            return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 根据传入的一组isbn，到Wish表中检索出相应的礼物，并且计算出某个礼物的wish心愿数
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched==False,
                        Wish.isbn.in_(isbn_list),Wish.status == 1).group_by(Wish.isbn).all()

        # 对象 字典
        count_list = [{'count':w[0], 'isbn':w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YushuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book

        # 对象代表一个礼物，具体
        # 类代表这个事物，它是抽象，不是具体的一个
    @classmethod
    def recent(cls):
        # 链式调用
        recent_gifts = cls.query.filter_by(launched=False).order_by(
            desc(Gift.create_time)).group_by(Gift.isbn).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()

        return recent_gifts

    # @classmethod
    # def get_wish_counts(cls, isbn_list):
    #     count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched==False,
    #                     Wish.isbn.in_(isbn_list),Wish.status == 1).group_by(Wish.isbn).all()
    #     count_list = [EachGiftWishCount(w[0], w[1]) for w in count_list]
    #     return count_list
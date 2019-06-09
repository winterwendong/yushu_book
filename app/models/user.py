# -*- coding:utf-8 -*-
from math import floor

from app.models.drift import Drift
from app.spider.yushu_book import YushuBook

__author__ = 'wendong'

from app.libs.enums import PendingStatus

from app.models.gift import Gift
from app.models.wish import Wish
from app.libs.helper import is_isbn_or_key

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy import String, Unicode, DateTime, Boolean
from sqlalchemy import SmallInteger, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import db, Base
from app import login_manager



class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    gifts = relationship('Gift')

    _password = Column('password', String(100), nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Drift.query.fiter(uid = self.id,
                                          launched=True).count()
        success_receive_count = Drift.query.filter(requester_id = self.id,
                                             pending=PendingStatus.success).count()
        return True if floor(success_gifts_count / 2) <= floor(success_receive_count) else False

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def can_satisfied_wish(self, current_gift_id = None):
        if current_gift_id:
            gift = Gift.query.get(current_gift_id)
            if gift.uid == self.id:
                return False
        if self.beans < 1:
            return False
        success_gifts = Drift.query.fiter(Drift.pending == PendingStatus.success,
                                          Gift.uid == self.id).count()
        success_receive = Drift.query.filter(Drift.pending == PendingStatus.success,
                                             Gift.requester.id == self.id).count()
        return False if success_gifts <= success_receive - 2 else True

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YushuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 即不在赠送清单，也不再心愿清单
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
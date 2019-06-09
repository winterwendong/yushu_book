# -*- coding:utf-8 -*-
from app.models.gift import Gift

__author__ = 'wendong'

from flask import render_template, config, current_app, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import web
from app.view_models.book import BookViewModel

@web.route('/')
def index():
    """
        首页视图函数
        这里使用了缓存，注意缓存必须是贴近index函数的
    """
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)
    # return 'hello'


# @web.route('/personal')
# @login_required
# def personal_center():
#     return render_template('personal.html', user=current_user.summary)



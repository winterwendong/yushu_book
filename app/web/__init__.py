# -*- coding:utf-8 -*-
from flask import Blueprint

__author__ = 'wendong'

from flask import render_template

# 蓝图blueprint
web = Blueprint('web', __name__)

# @web.app_errorhandler(404)
# def not_found(e):
    # AOP思想， 面向切片编程
    # return render_template('404.html'), 404

from app.web import book
from app.web import auth
from app.web import gift
from app.web import wish
from app.web import main


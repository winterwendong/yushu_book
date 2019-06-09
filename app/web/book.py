# -*- coding:utf-8 -*-
from flask import jsonify, request, render_template, flash
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YushuBook
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from flask_login import current_user

from . import web
from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish

__author__ = 'wendong'
__data__ = '2019-05-11 17:13'



@web.route('/test')
def test():
    r = {
        'name': '',
        'age': 18
    }
    flash('hello,wendong')
    return render_template('test.html', data=r)

@web.route('/book/search')
def search():
    """
        q: 普通关键字或isbn
        page:
        ?q=金庸&page=1
        isbn isbn13 isbn13个0到9的数字组成
        isbn10 10个0到9的数字组成，含有一些' - '
    """
    # Request Response
    # HTTP的请求信息
    # 查询参数 POST参数 remote ip

    # isbn isbn13 isbn13个0到9的数字组成
    # isbn10 10个0到9的数字组成，含有一些' - '

    # q = request.args['q']
    # page = request.args['page']

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YushuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)

    else:
        flash("搜索的关键字不符合要求，请重新输入关键字")
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    """
            1. 当书籍既不在心愿清单也不在礼物清单时，显示礼物清单
            2. 当书籍在心愿清单时，显示礼物清单
            3. 当书籍在礼物清单时，显示心愿清单
            4. 一本书要防止即在礼物清单，又在赠送清单，这种情况是不符合逻辑的

            这个视图函数不可以直接用cache缓存，因为不同的用户看到的视图不一样
            优化是一个逐步迭代的过程，建议在优化的初期，只缓存那些和用户无关的“公共数据"
    """
    has_in_gifts = False
    has_in_wishs = False

    # 取书籍详情数据
    yushu_book = YushuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True

        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishs = False


    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishs = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_models = TradeInfo(trade_gifts)
    trade_wishs_models = TradeInfo(trade_wishs)

    return render_template('book_detail.html', book=book,
                           has_in_gifts=has_in_gifts,
                           has_in_wishs=has_in_wishs,
                           wishes=trade_wishs_models,
                           gifts=trade_gifts_models)
# -*- coding:utf-8 -*-
import json

__author__ = 'wendong'
__data__ = '2019-05-13 18:26'

from app.libs.helper import get_isbn


class BookViewModel:
    def __init__(self, data):
        self.title = data['title']
        self.author = '、'.join(data['author'])
        self.binding = data['binding']
        self.publisher = data['publisher']
        self.image = data['image']
        self.price = '￥' + data['price'] if data['price'] else data['price']
        self.isbn = get_isbn(data)
        self.pubdate = data['pubdate']
        self.summary = data['summary']
        self.pages = data['pages']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])

        return '/'.join(intros)

class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = None

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]
        self.keyword = keyword

class _BookViewModel:
    # 描述特征（类变量、实例变脸）
    # 行为（方法）
    # 面向过程
    @classmethod
    def package_singal(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
            print(returned['books'])
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data["title"],
            'publisher': data["publisher"],
            'pages': data["pages"] or "",
            'price': data["price"],
            'author': "、".join(data["author"]),
            'summary': data["summary"] or "",
            'image': data["image"],
        }
        print(book)
        return book

    @classmethod
    def __cut_books_data(cls, data):
        books = []
        for book in data['books']:
            r = {
                'title': data['title'],
                'publisher': data['publisher'],
                'pages': data['pages'],
                'price': data['price'],
                'author': '、'.join(data['author']),
                'summary': data['summary'],
                'image': data['image'],
            }
            books.append(r)
        return books
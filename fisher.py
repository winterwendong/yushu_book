# -*- coding:utf-8 -*-
from app import create_app


__author__ = 'wendong'


app = create_app()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0')


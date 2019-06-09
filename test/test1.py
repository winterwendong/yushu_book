# -*- coding:utf-8 -*-
import threading
import time

__author__ = 'wendong'
__data__ = '2019-05-13 17:05'

from werkzeug.local import LocalStack

# 使用线程隔离的意义在于：使当前线程能够正确引用到他自己所创建的对象，而不是引用到其他线程所创建的对象

my_stack = LocalStack()
my_stack.push(1)
print('in main thraed after push, value is:' + str(my_stack.top))

def worker():
    print('in new thraed before push, value is:' + str(my_stack.top))
    my_stack.push(2)
    print('in new thraed after push, value is:' + str(my_stack.top))


new_t = threading.Thread(target=worker)
new_t.start()
time.sleep(1)

# 主线程
print('in main thraed value is:' + str(my_stack.top))
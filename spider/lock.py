# -*- coding: utf-8 -*-
import threading

lock = threading.RLock()


def my_print():
    print('start')
    lock.acquire()
    lock.acquire()
    print('try rlock')
    lock.release()
    lock.release()


if __name__ == '__main__':
    my_print()
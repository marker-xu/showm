# -*- coding: utf-8 -*-

import time
import threading


zero = 0
r_lock = threading.Lock()


def thread_main(num):
    print num


def papa(num):
    for i in range(num):
        yield i


def test(num):

    threads = []
    red = papa(num)
    for x in xrange(0, num):
        threads.append(threading.Thread(target=thread_main, args=(red.next(),)))

    for t in threads:
        t.start()
        print "%s-%d"%(t.getName(), t.isDaemon())

    print("start-%d"%threading.activeCount())
    for t in threads:
        t.join()
    print("end-%d"%threading.activeCount())


def change_zero():
    global zero
    for i in range(1000000):
        r_lock.acquire()
        zero = zero + 1
        zero = zero - 1
        r_lock.release()


if __name__ == '__main__':
    t = time.time()
    test(4)
    print(time.time() - t)

    th1 = threading.Thread(target = change_zero)
    th2 = threading.Thread(target = change_zero)
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    print(zero)
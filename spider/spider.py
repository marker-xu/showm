# -*- coding: utf-8 -*-
import time
import threading
from queue import Queue, Empty
import json


def run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print('running', end-start, 's')
    return wrapper


class Spider():
    """
    基类
    """

    def __init__(self):
        self.queue_tasks = Queue()
        self.data = list()
        self.thread_num = 5
        self.running = True
        self.filename = False
        self.output_result = True

    def start_requests(self):
        yield (self.start_url, self.parse)

    def start_req(self):
        for task in self.start_requests():
            self.queue_tasks.put(task)

    def parses(self):
        print(threading.current_thread().name, 'starting')
        while self.running or not self.queue_tasks.empty():
            print self.queue_tasks.qsize()
            try:
                url, func = self.queue_tasks.get(timeout=3)
                print('crawling', url)
                for task in func(url):
                    print type(task)
                    if isinstance(task, tuple):
                        self.queue_tasks.put(task)
                    elif isinstance(task, dict):
                        if self.output_result:
                            print(task)
                        print "ret: "
                        print(task)
                        self.data.append(task)
                    else:
                        raise TypeError('parse functions have to yield url-function tuple or data dict')
            except Empty:
                print('{}: Timeout occurred'.format(threading.current_thread().name))
            except TypeError:
                print "'NoneType' object is not iterable"
        print(threading.current_thread().name, 'finished')

    @run_time
    def run(self):
        ths = []

        th1 = threading.Thread(target=self.start_req)
        th1.start()
        ths.append(th1)
        for _ in range(self.thread_num):
            th = threading.Thread(target=self.parses)
            th.start()
            ths.append(th)

        for th in ths:
            th.join()

        if self.filename:
            s = json.dumps(self.data, indent=4)
            with open(self.filename, 'w') as f:
                f.write(s)

        print('Data crawling is finished.')
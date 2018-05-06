# coding: utf-8

import os
import random
import time
from multiprocessing import Pool, Manager


# 开启进程池
# 通过queue进行进程之间的通信


def start_one_process(first, queue):
    """
    存入数据
    :param first:
    :param queue:
    :return:
    """
    print("Run child process {0} {1}".format(first, os.getpid()))
    start = time.time()
    queue.put("I am process {}".format(first))
    time.sleep(random.random()*3)
    end = time.time()
    print("Process {0} run {1}".format(first, end - start))


def queue_read(queue):
    """
    读取进程之间通信的值
    死循环进行持续读取
    :param queue:
    :return:
    """
    print("Read process {}".format(os.getpid()))
    while True:
        print("Get value {}".format(queue.get(True)))


def start_process(func, read, num=1):
    """
    开启多进程
    :param func: 函数
    :param read: 读取消息队列函数
    :param num: 进程数
    :return:
    """
    print("Run task {}".format(os.getpid()))
    q = Manager().Queue()
    p = Pool(num)
    for i in range(1, num):
        p.apply_async(func, args=(i, q))
    p.apply_async(read, args=(q,))
    print("Waiting for all subprocess done...")
    p.close()
    p.join()
    print("All subprocess done...")


if __name__ == '__main__':
    start_process(start_one_process, queue_read, 4)



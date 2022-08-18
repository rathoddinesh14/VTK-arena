#!/usr/bin/env python

from multiprocessing import Process, Pool


def func(arg):
    print(arg)
    # wait for 20 sec
    n = 10000000
    while n > 0:
        n -= 10
        print(n)


if __name__ == '__main__':


    proc_pool = Pool(processes=2)

    num_task = 10

    print("Number of Tasks: ", num_task)

    data = {}
    for i in range(num_task):
        data[i] = i

    # assign tasks to processes
    for i in range(num_task):
        proc_pool.apply_async(func, args=(data[i],))

    # close the pool and wait for the work to finish
    proc_pool.close()
    proc_pool.join()
    print("All Tasks have been completed")
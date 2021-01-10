# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 12:32:35 2021

@author: 40737
"""

import time
import os
from threading import Thread, current_thread
from multiprocessing import Process, current_process

COUNT = 200000000
SLEEP = 10

def io_bound(sec):
    
    pid = os.getpid()
    thread_name = current_thread().name
    process_name = current_process().name
    
    print(f"{pid} * {process_name} * {thread_name}->>> Start sleeping...")
    time.sleep(sec)
    print(f"{pid} * {process_name} * {thread_name}->>> Finished sleeping...")
    
def cpu_bound(n):
    
    pid = os.getpid()
    thread_name = current_thread().name
    process_name = current_process().name
    print(f"{pid} * {process_name} * {thread_name}->>> Start sleeping...")
    
    while n>0:
        n -=1
    print(f"{pid} * {process_name} * {thread_name} ---> Finished counting...")
    

def sequential():
    """
    Part 1: Running IO-bound task twice, one after the other…
    """
    io_bound(SLEEP)
    io_bound(SLEEP)
    
    
def threading_run_IO_bound_tasks():
    """
    Part 2: Using threading to run the IO-bound tasks…
    """
    
    t1 = Thread(target = io_bound, args = (SLEEP,))
    t2 = Thread(target = io_bound, args= (SLEEP,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def cpu_bound_sequential():
    """
    Part 3: Running CPU-bound task twice, one after the other…
    """
    cpu_bound(COUNT)
    cpu_bound(COUNT)
    
def threading_for_CPU_bound_tasks():
    """
    Part 4: Can threading speed up our CPU-bound tasks>?
    """
    t1 = Thread(target = cpu_bound, args = (COUNT,))
    t2 = Thread(target = cpu_bound, args = (COUNT,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def multi_process_for_cpu_bound_tasks():
    p1 = Process(target = cpu_bound, args = (COUNT,))
    p2 = Process(target = cpu_bound, args = (COUNT,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    start = time.time()   
    sequential()    
    end = time.time() 
    print('Time taken in seconds was {} for sequential method -'.format(end - start))
    print()
    start = time.time()
    threading_run_IO_bound_tasks()
    end = time.time()
    print('Time taken in seconds was {} for threading_run_IO_bound_tasks method -'.format(end - start))
    print()
    start = time.time()
    cpu_bound_sequential()
    end = time.time()
    print('Time taken in seconds was {} for cpu_bound_sequential method -'.format(end - start))
    print()
    start= time.time()
    threading_for_CPU_bound_tasks()
    end = time.time()
    print('Time taken in seconds was {} for threading_for_CPU_bound_tasks method -'.format(end - start))
    print()
    start= time.time()
    multi_process_for_cpu_bound_tasks()
    end = time.time()
    print('Time taken in seconds was {} for multi_process_for_cpu_bound_tasks method -'.format(end - start))
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    




    
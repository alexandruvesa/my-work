# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:25:25 2020

@author: Alex
"""

import logging
import threading 
import time

def thread_function(name):
    logging.info('Thread %s: starting', name)
    time.sleep(2)
    logging.info("Thread %2: finishing", name)
    
    
if __name__ =="__main__":
    format =  "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    logging.info("Main : before creating thread")
    x = threading.Thread(target = thread_function, args=(1,))
    logging.info("Main :before running thread")
    x.start()
    logging.info("Main : wait for the thread to finish")
    
    #If you want a thread to wait for another thread to finish you have to use join()
    x.join()
    logging.info("Main :all done")
    
    x = threading.Thread(target=thread_function, args=(1,))
    x.start()

      
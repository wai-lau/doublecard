import os
import sys
from datetime import datetime

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def clock(func, times = 1):
   def func_wrapper(*args):
       dt = datetime.now()
       result = None
       blockPrint()
       for _ in range(times - 1):
            result = func(*args)
       enablePrint()
       result = func(*args)
       dt2 = datetime.now()
       print("-{}- took{} {}μs with args type {}"
             .format(func.__name__,
                     " on average" if times != 1 else "",
                     ((dt2-dt).seconds*1000000 + (dt2-dt).microseconds)/times,
                     type(args)))
       return result
   return func_wrapper

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
   def func_wrapper(*args, **kwargs):
       dt = datetime.now()
       result = None
       blockPrint()
       for _ in range(times - 1):
            result = func(*args, **kwargs)
       enablePrint()
       result = func(*args, **kwargs)
       dt2 = datetime.now()
       print("-{}- took{} {}ms with args type {}"
             .format(func.__name__,
                     " on average" if times != 1 else "",
                     round((dt2-dt).seconds*1000 + (dt2-dt).microseconds/1000, 3)/times,
                     type(args)))
       return result
   return func_wrapper

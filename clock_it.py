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
   def func_wrapper(args=None):
       dt = datetime.now().microsecond
       result = None
       blockPrint()
       for _ in range(times - 1):
           if not args:
               result = func()
           if args:
               result = func(args)
       enablePrint()
       if not args:
           result = func()
       if args:
           result = func(args)
       dt2 = datetime.now().microsecond
       print("-{}- took {}μs with args type {}"
             .format(func.__name__,
                     int(dt2)-int(dt),
                     type(args)))
       return result
   return func_wrapper



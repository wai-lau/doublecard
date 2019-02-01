from datetime import datetime
def clock(func):
   def func_wrapper(args=None):
       dt = datetime.now().microsecond
       result = func(args)
       dt2 = datetime.now().microsecond
       print("-{}- took {}μs with args type {}"
             .format(func.__name__, dt2-dt, type(args)))
       return result
   return func_wrapper

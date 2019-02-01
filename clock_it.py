from datetime import datetime
def clock_it(func):
   def func_wrapper(args):
       dt = datetime.now().microsecond
       result = func(args)
       dt2 = datetime.now().microsecond
       print("-{}- took {}ms with args type {}"
             .format(func.__name__, dt2-dt, type(args)))
       return result
   return func_wrapper



import time

def warpper():
    def cost(func):
        def inner(*args,**kwargs):
            startTime = time.time()
            func(*args,**kwargs)
            endTime = time.time()
            costTime = endTime - startTime
            print(costTime)
        return inner
    return cost

@warpper
def fib(n):
    if n ==1 or n ==2:
        return 1
    return fib(n-1) + fib(n-2)


print(fib(10))
from django.test import TestCase

# Create your tests here.
from django.contrib.auth.hashers import check_password
def foo(n,result=1):
    if n == 1:
        return result
    else:
        return n * (n-1)

print(foo(5))


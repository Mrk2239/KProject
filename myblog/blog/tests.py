from django.test import TestCase

# Create your tests here.
alist = [1,2,3,4,5]
a=sum([alist[i]**2 for i in range(0,len(alist),2)])
print(a)

# 0 , 1 ,2 ,3,4,5
for i in range(0,6,2):
    print(i)
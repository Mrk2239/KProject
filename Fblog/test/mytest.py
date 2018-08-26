import random
import string

from werkzeug.security import generate_password_hash,check_password_hash

# from app.views.main import mainbp
# from app.views import mainbp
# from app import mainbp

from app.models import User


if __name__ == '__main__':
    # print(generate_password_hash('123456'))
    # print(check_password_hash('pbkdf2:sha256:50000$gP3zZyxG$aec274a3f41d1706e2367aa85d1c9b6762d8cc5fcb0d32db1b5c34c267d7da01','123456'))

    # u = User(username='fuck',password='123456')
    # print(u.password)

    # u = User(username='fuck',pwd='123456')
    # print(u.pwd)

    population = string.ascii_lowercase+string.ascii_uppercase+string.digits
    # print(population)

    name = random.sample(population,32)
    print(''.join(name))

    pass


class Person:

    uname = 'None'
    def __init__(self,uname):
        self.uname = uname

    def fuck(self):
        print(self.uname + 'is fucking....')

zs = Person('zs')
lisi = Person('lisi')

zs.fuck()
lisi.fuck()
import string
import random
import threading

def create_random_code():
    chars=string.ascii_uppercase + string.digits
    size = 10
    code = ''.join(random.choice(chars) for _ in range(size))
    while User.query.filter_by(invitationCode=code).first():
        code = ''.join(random.choice(chars) for _ in range(size))
    return code

def set_interval(func, sec):
    def func_wrapper():
        set_interval((func), sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
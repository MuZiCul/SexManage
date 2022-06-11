import random
import string


def getRandomLD(length):
    strs = ""
    num = string.ascii_letters + string.digits
    for i in range(length):
        strs += random.choice(num)
    return strs


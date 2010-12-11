from random import randint

numerals = '0123456789abcdefghjklmnopqrstvwxyzABCDEFGHJKLMNOPQRSTVWXYZ'
base = len(numerals)
def hashint(num):
    if num == 0: return '0'

    if num < 0:
        sign = '-'
        num = -num
    else:
        sign = ''

    result = ''
    while num:
        result = numerals[num % (base)] + result
        num //= base

    return sign + result


def gen_key():
    return hashint(abs(randint(100,90000)))


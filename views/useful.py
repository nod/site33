from random import randint
import re

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


def hash_val(val):
    import hashlib
    return hashlib.md5(val.lower().strip()).hexdigest()


def avatar_url(email):
    eml = hash_val(email)
    print "EML is", eml
    return 'http://www.gravatar.com/avatar/{}?s=200'.format(eml)


def gen_key():
    return hashint(abs(randint(100,90000)))

# slugify from http://code.activestate.com/recipes/577257-slugify-make-a-string-usable-in-a-url-or-filename/

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)




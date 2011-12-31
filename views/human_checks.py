from random import choice, shuffle

big_list = {
    'elvis': 'Elvis',
    'texas': 'Texas',
    'alaska': 'Alaska',
    'deficit': 'The Deficit',
    'oprah': 'Oprah Winfrey',
    'huge': 'Something Huge',
    }

small_list = {
    'lemon': 'A Lemon',
    'orange': 'An Orange',
    'kittens': 'Kittens',
    'backpack': 'A Backpack',
    'ipod': 'An iPod Nano',
    'fork': 'An Average Fork',
    'spoon': 'An Average Spoon',
    'pillow': 'A throw pillow',
    'toes': 'Your pinky toe',
    'eye': 'Your left eye',
    'nostril': 'Your right nostril',
    }

def build_list():
    big_ = choice(big_list.keys())
    tmp = { big_: big_list[big_] }
    while len(tmp) < 5:
        lil_ = choice(small_list.keys())
        if lil_ not in tmp:
            tmp[lil_] = small_list[lil_]
    tmp_ = [ (k,v) for k,v in tmp.iteritems() ]
    shuffle(tmp_)
    return tmp_

def verify(x):
    return x in big_list or x == 'yom0mMa'

#!/usr/bin/env python

import re

import tokyo.cabinet as tc

from datetime import datetime

key_Sorted = '_x_sorted_posts'

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

class BogusBlogDB(Exception): pass

class Blog(object):

    def __init__(self, dbpath, metapath, initialize=False):
        self._db = tc.TDB()
        self._db.open(dbpath)
	self._dbmeta = tc.HDB()
	self._dbmeta.open(metapath, tc.TDBOCREAT)
        # check that we have desirable members and not an empty db
        if initialize:
 		self._dbmeta[key_Sorted] = []

    def __del__(self):
        if self._db: self._db.close()
	if self._dbmeta: self._dbmeta.close()

    def __iter__(self):
        for p in self._db.get(key_Sorted, []):
            yield self._db.get(p)

    def __getitem__(self, key):
        """
        this is overloaded a bit to make things pretty simple.  Slices will
        return an iterator of the objects requested or direct by key returns
        the actual post.
        """
        if type(key) == slice:
            # slc = slice(*(key.indices(len(self._db.get(key_Sorted)))))
            return (self._db[k] for k in self._db[key_Sorted][key])
        elif type(key) == int:
            return self._db[self._db[key_Sorted][key]]
        else: return self._db[key]

    def _create_sorted(self):
        self._db[key_Sorted] = [ str(k['key']) for k in \
            sorted(
                filter(
                    lambda x: type(x) == dict,
                    self._db.values()
                    ),
                key = lambda p:p['date'],
                reverse = True
                ) ]

    def new(self, title, content, date=None, tags=None):
        slug = str(slugify(title))
        while self._db.has_key(slug): slug += '_'
        tmp = {
            'key': slug,
            'title': title,
            'date': date or datetime.now(),
            'content': content,
            'tags': tags or [],
            }
        db[slug] = tmp
        self._create_sorted()
        self._db.sync()
        return tmp

    def remove_post(self, key):
        del self._db[key]
        self._create_sorted()
        self._db.sync()


#!/usr/bin/env python

import re
from json import dumps, loads

import tokyo.cabinet as tc

from datetime import datetime

from useful import slugify

key_Sorted = '_x_sorted_posts'

class BogusBlogDB(Exception): pass


class Blog(object):

    def __init__(self, dbpath, metapath, writeable=False):
        if writeable: flags =  tc.TDBOWRITER|tc.TDBOCREAT
        else: flags =  tc.TDBOCREAT

        self._db = tc.TDB()
        self._db.open(dbpath, flags)

        self._dbmeta = tc.HDB()
        self._dbmeta.open(metapath, flags)

        # check that we have desirable members and not an empty db
        if key_Sorted not in self._dbmeta:
            self._create_sorted()

    def __contains__(self, key):
        return key in self._db

    def __del__(self):
        if self._db: self._db.close()
        if self._dbmeta: self._dbmeta.close()

    def __iter__(self):
        sorted_keys = loads(self._dbmeta[key_Sorted])
        for p in sorted_keys: yield self._db[p]

    def _post(self, d):
        try:
            d['date'] = datetime(*loads(d['date'])[:6])
        except:
            d['date'] = datetime.now()
        d['tags'] = [t.strip() for t in loads(d['tags'])]
        return d

    def __setitem__(self, key, value):
        """
        assigns a dictionary to a key. this is dangerous right now...
        you should use .new(...) for any new posts but if you're working on an
        existing post, just assign it back and this will grab it and splat it
        in place.
        """
        self.new(**value)

    def __getitem__(self, key):
        """
        this is overloaded a bit to make things pretty simple.  Slices will
        return an iterator of the objects requested or direct by key returns
        the actual post.
        """
        if type(key) == slice:
            # slc = slice(*(key.indices(len(self._db.get(key_Sorted)))))
            slc = key
            sorted_keys = loads(self._dbmeta[key_Sorted])
            return (self._post(self._db[k]) for k in sorted_keys[slc])
        elif type(key) == int:
            sorted_keys = loads(self._dbmeta[key_Sorted])
            return self._post(self._db[sorted_keys[key]])
        else: return self._post(self._db[key])

    def _create_sorted(self):
        q = self._db.query()
        q.sort('date', tc.TDBQOSTRDESC)
        sorted_keys = self._db.metasearch((q,), tc.TDBMSUNION)
        self._dbmeta[key_Sorted] = dumps(sorted_keys)
        self._dbmeta.sync()

    def meta_list(self):
        """ returns a tuple (years, tags) """
        years = set()
        tags = set()
        for p in self._db:
            post = self._post(self._db[p])
            years.add(post['date'].year)
            for t in post['tags']:
                tags.add(t)
        return (
            sorted(years, reverse=True),
            sorted(tags, cmp=lambda x,y: cmp(x.lower(), y.lower())) 
            )

    def all_posts(self, year=None):
        q = self._db.query()
        q.sort('date', tc.TDBQOSTRDESC)
        if year:
            q.filter('date', tc.TDBQCSTRINC, '[%d'%year)
        all_posts = self._db.metasearch((q,), tc.TDBMSISECT)
        return ( self._post(self._db[t]) for t in all_posts )

    def posts_with_tag(self, tag):
        q = self._db.query()
        q.sort('date', tc.TDBQOSTRDESC)
        q.filter('tags', tc.TDBQCSTRINC, tag)
        tag_keys = self._db.metasearch((q,), tc.TDBMSISECT)
        return ( self._post(self._db[t]) for t in tag_keys )

    def new(self, title, content, date=None, tags=None, key=None):
        slug = key or str(slugify(title))
        if not key: # assume this is new
            while slug in self._db: slug += '_'
        tmp = {
            'key': slug,
            'title': title,
            'date': dumps((date or datetime.now()).timetuple()[:]),
            'content': content,
            'tags': dumps(tags or []),
            }
        self._db[slug] = tmp
        self._create_sorted()
        return tmp

    def remove_post(self, key):
        del self._db[key]
        self._create_sorted()
        self._db.sync()


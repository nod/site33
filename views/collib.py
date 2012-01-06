#!/usr/bin/env python

import re
from datetime import datetime

from iso8601 import parse_date, ParseError as DateParseError
from databag import DataBag

from useful import slugify


class DataBagMember(object):

    def __init__(self, slug, c_at=None, tags=None, **kwa):

        if not isinstance(slug, basestring):
            raise ValueError('slug is required and must be basestring')

        if tags and not hasattr(tags, '__iter__'):
            raise ValueError('tags is not one of: list, tuple, set')

        if c_at and not isinstance(c_at, datetime):
            try: c_at = parse_date(c_at)
            except DateParseError:
                raise ValueError('c_at must be a datetime or iso8601 str')

        self.slug = slug
        self.c_at = c_at or datetime.now()
        self.tags = tags or tuple()

    @classmethod
    def _d_members(cls):
        """
        override in children to provide storage mechanism for members.  we do it
        this way so that the keys can be short and we can format data coming
        out.

        reserved keys: c, s

        format: ('key', 'attr_name', fmt func to json, fmt func from json)
        either fmt function can be None and return the value directly
        """
        return tuple()

    def _d(self):
        """
        To dictionary.
        Return a dictionary suitable for jsonification or databaggery
        """
        tmp_ = dict(s = self.slug, c = self.c_at)
        if self.tags: tmp_['tg'] = self.tags
        mems = self._d_members()
        for x in self._d_members():
            k,attr,fmt_to,fmt_from = x
            if not hasattr(fmt_to, '__call__'):
                fmt_to = lambda j:j
            tmp_[k] = fmt_to(getattr(self, attr))
        return tmp_

    @classmethod
    def _fd(cls, d):
        """
        from dictionary. create instance from a member from a dict previously
        created by inst._d()
        """
        tmp_ = dict(slug=d.get('s'), c_at=d.get('c'), tags=d.get('tg'))
        for x in cls._d_members():
            k,attr,fmt_to,fmt_from = x
            fmt_from = fmt_from or (lambda j:j)
            tmp_[attr] = d.get(k)
        return cls(**tmp_)

    def get(self, attr, default=None):
        """
        return the attr requested or None, just like a dictionary does it.
        purely convenience method.
        """
        return getattr(self, attr, default)


class DataBagCollection(object):

    def __init__(self, fpath, tblname=None):
        self._db = DataBag(fpath, tblname or 'dbc')

    def _member(self, k, d):
        """
        children can overwrite this to return anything out of the collection
        """
        return DataBagMember._fd(d)

    def __contains__(self, key_or_obj):
        if isinstance(key_or_obj, DataBagMember):
            return key_or_obj.slug in self._db
        else:
            return key_or_obj in self._db

    def __iter__(self):
        for k,d in self._db.by_created():
            yield self._member(k,d)

    def meta_lists(self):
        """ returns a tuple (years, tags) """
        tags, years = set(), set()
        for p in self:
            years.add(p.c_at.year)
            tags.update(p.tags)
        return (
            sorted(years, reverse=True),
            sorted(tags, cmp=lambda x,y: cmp(x.lower(), y.lower()))
            )

    def _sorted_members(self, iter):
        return sorted(
            iter,
            cmp = lambda x,y: cmp(x.c_at, y.c_at),
            reverse = True
            )

    def all_members(self, year=None):
        """ returns list of posts, limited to year if requested """
        return self._sorted_members(
            p for p in self if (True if not year else year == p.c_at.year)
            )

    def members_with_tag(self, tag):
        return self._sorted_members(p for p in self if (tag in p.tags))

    def member(self, slug):
        return self._member(slug, self._db[slug])

    def save(self, member):
        print "BLEH"
        self._update_member(member.slug, member._d())

    def remove(self, slug_or_mem):
        if isinstance(slug_or_mem, DataBagMember): slug = slug_or_mem.slug
        else: slug = slug_or_mem
        del self._db[slug]

    def _update_member(self, slug, d):
        self._db[slug] = d



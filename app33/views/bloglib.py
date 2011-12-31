#!/usr/bin/env python

import re
from datetime import datetime

from iso8601 import parse_date
from databag import DataBag

from useful import slugify


class BlogPost(object):
    __slots__ = ('title', 'text', 'tags', 'c_at')

    def __init__(self, title, body, tags=None, c_at=None):

        self.title = title
        self.body = body
        self.tags = tags or tuple()
        self.c_at = c_at or datetime.now()

        if not isinstance(datetime, self.c_at)
            raise ValueError('c_at must be a datetime')

        if not isinstance(self.tags, (list, tuple, set)):
            raise ValueError('tags is not one of: list, tuple, set')

    def _d(self):
        """
        To dictionary.
        Return a dictionary suitable for jsonification or databaggery
        """
        return dict(
            t = self.title,
            b = self.body,
            tg = self.tags,
            c = self.c_at,
            )

    @classmethod
    def _fd(self, d):
        """
        From dictionary.
        Create an instance of a BlogPost from a dictionary created by inst._d()
        """
        return BlogPost(
            title = d.get('t'),
            body  = d.get('b'),
            tags = d.get('tg'),
            c_at = parse_date(d.get('c')),
            )


class Blog(object):

    def __init__(self, fpath):
        self._dbposts = DataBag(fpath, 'blog')

    def __contains__(self, key):
        return key in self._dbposts

    def __iter__(self):
        return (BlogPost._fd(p) for p in self._dbposts)

    def meta_list(self):
        """ returns a tuple (years, tags) """
        tags, years = set(), set()
        for p in self:
            years.add(p.c_at.year)
            tags.update(p.tags)
        return (
            sorted(years, reverse=True),
            sorted(tags, cmp=lambda x,y: cmp(x.lower(), y.lower()))
            )

    def _sorted_posts(self, iter):
        return sorted(
            iter,
            cmp = lambda x,y: cmp(x.c_at, y.c_at),
            reverse = True
            )

    def all(self, year=None):
        """ returns list of posts, limited to year if requested """
        return self._sorted_posts(
            p for p in self if (True if not year else year == p.c_at.year)
            )

    def posts_with_tag(self, tag):
        return self._sorted_posts(p for p in self if (tag in p.tags))

    def new(self, title, content, tags=None):
        slug = key or str(slugify(title))
        if not key: # assume this is new
            while slug in self._db: slug += '_'
        post_ = BlogPost(
            title,
            content,
            tags,
            )
        self._dbposts[slug] = post_._d()
        return post_

    def remove_post(self, key):
        del self._dbposts[key]



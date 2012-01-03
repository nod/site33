#!/usr/bin/env python

import re
from datetime import datetime

from iso8601 import parse_date
from databag import DataBag

from useful import slugify


class BlogPost(object):
    def __init__(self, title, text, tags=None, c_at=None, slug=None):
        self.title = title
        self.text = text
        self.tags = tags or tuple()
        self.c_at = c_at or datetime.now()
        self.slug = slug

        if len(self.title) < 1:
            raise ValueError('title too short "{}"')

        if not isinstance(self.c_at, datetime):
            raise ValueError('c_at must be a datetime')

        if not isinstance(self.tags, (list, tuple, set)):
            raise ValueError('tags is not one of: list, tuple, set')

    def _d(self):
        """
        To dictionary.
        Return a dictionary suitable for jsonification or databaggery
        """
        return dict(
            s = self.slug,
            t = self.title,
            b = self.text,
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
            slug = d.get('s'),
            title = d.get('t'),
            text  = d.get('b'),
            tags = d.get('tg'),
            c_at = parse_date(d.get('c')),
            )

    def get(self, attr, default=None):
        """
        return the attr requested or None, just like a dictionary does it.
        purely convenience method.
        """
        return getattr(self, attr, default)


class Blog(object):

    def __init__(self, fpath):
        self._dbposts = DataBag(fpath, 'blog')

    def __contains__(self, key):
        return key in self._dbposts

    def __iter__(self):
        return (BlogPost._fd(d) for p,d in self._dbposts.by_created())

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

    def _sorted_posts(self, iter):
        return sorted(
            iter,
            cmp = lambda x,y: cmp(x.c_at, y.c_at),
            reverse = True
            )

    def all_posts(self, year=None):
        """ returns list of posts, limited to year if requested """
        return self._sorted_posts(
            p for p in self if (True if not year else year == p.c_at.year)
            )

    def posts_with_tag(self, tag):
        return self._sorted_posts(p for p in self if (tag in p.tags))

    def post(self, slug):
        return BlogPost._fd(self._dbposts[slug])

    def new_post(self, title, content, tags=None, c_at=None):
        if not isinstance(c_at, datetime): c_at = datetime.now()
        slug = '{}-{}'.format(c_at.year, str(slugify(title)))
        print slug, c_at
        while slug in self._dbposts: slug += '_'
        post_ = BlogPost(
            title = title,
            text = content,
            tags = tags,
            slug = slug,
            c_at = c_at,
            )
        self._dbposts[slug] = post_._d()
        return slug, post_

    def update_post(self, post):
        """
        updates a post's data.
        does NOT modify the slug
        """
        self._dbposts[post.slug] = post._d()

    def remove_post(self, slug):
        del self._dbposts[slug]



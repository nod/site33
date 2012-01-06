#!/usr/bin/env python

import re
from datetime import datetime

from iso8601 import parse_date

from useful import slugify
from collib import DataBagCollection, DataBagMember


class BlogPost(DataBagMember):
    def __init__(self, title, text, **kwa):

        DataBagMember.__init__(self, **kwa)
        self.title = title
        self.text = text

        if len(self.title) < 1:
            raise ValueError('title too short')

    @classmethod
    def _d_members(cls):
        return (
            ('t', 'title', None, None),
            ('b', 'text', None, None),
            )


class Blog(DataBagCollection):

    def __init__(self, fpath):
        DataBagCollection.__init__(self, fpath, 'blog')

    def _member(self, k, d):
        return BlogPost._fd(d)

    def new_post(self, title, content, tags=None, c_at=None):
        if not isinstance(c_at, datetime): c_at = datetime.now()
        slug = '{}-{}'.format(c_at.year, str(slugify(title)))
        while slug in self: slug += '_'
        post_ = BlogPost(
            title = title,
            text = content,
            tags = tags,
            slug = slug,
            c_at = c_at,
            )
        self.save(post_)
        return slug, post_

    def posts(self, year=None):
        return self.all_members(year)

    def posts_with_tag(self, tag):
        return self.members_with_tag(tag)

    def post(self, slug):
        return self.member(slug)




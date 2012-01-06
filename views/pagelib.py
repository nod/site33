#!/usr/bin/env python

import re
from datetime import datetime

from iso8601 import parse_date
from databag import DataBag

from collib import DataBagCollection, DataBagMember
from useful import slugify


class Page(DataBagMember):
    """
    Page( ... )
        required params: title, text
        optional params: slugs, tags, c_at
    """
    def __init__(self, title, text, **kwa):
        DataBagMember.__init__(self, **kwa)
        self.title = title
        self.text = text

    @classmethod
    def _d_members(self):
        return (
            ('t', 'title', None, None),
            ('x', 'text', None, None),
            )


class Book(DataBagCollection):

    def __init__(self, fpath):
        DataBagCollection.__init__(self, fpath, 'book')

    def _member(self, k, d):
        return Page._fd(d)

    def new_page(self, title, text, tags=None, slug=None):
        self.save( Page(title=title, text=text, tags=tags, slug=slug) )

    def page(self, slug):
        return self.member(slug)


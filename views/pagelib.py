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
        optional params: slugs, tags, c_at, creator_name
    """
    def __init__(
            self, title, text, cr_name=None, cr_avatar=None,
            owner_only=False, **kwa
            ):
        DataBagMember.__init__(self, **kwa)
        self.title = title
        self.text = text
        self.cr_name = cr_name
        self.cr_avatar = cr_avatar
        self.owner_only = owner_only

    @classmethod
    def _d_members(self):
        return (
            ('t', 'title', None, None),
            ('x', 'text', None, None),
            ('crn', 'cr_name', None, None),
            ('cra', 'cr_avatar', None, None),
            ('oo', 'owner_only', None, None),
            )


class Book(DataBagCollection):

    def __init__(self, fpath):
        DataBagCollection.__init__(
            self,
            fpath,
            'book',
            versioned=True,
            history=30
            )

    def _member(self, k, d):
        return Page._fd(d)

    def new_page(
            self, title, text, tags=None, slug=None,
            cr_name=None, cr_avatar=None, owner_only=False):
        self.save(
                Page(
                    title=title, text=text, tags=tags, slug=slug,
                    cr_name=cr_name, cr_avatar=cr_avatar,
                    owner_only=owner_only
                    )
                )

    def page(self, slug):
        return self.member(slug)

    def page_authors(self, slug):
        """
        gross method that rips through old versions of a doc and builds a set of
        (nick, avatar) for authors of versions of the doc. very non-optimal way
        of doing this...
        """

        a_ = set()
        version = 0
        while 1:
            try:
                p = self.member(slug, version=version)
                a_.add((p.cr_name, p.cr_avatar))
                version -= 1
            except KeyError:
                break # no more versions of the doc

        return a_


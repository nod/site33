
import unittest
from datetime import datetime, timedelta

from . import pagelib

class TestBookLib(unittest.TestCase):

    def setUp(self):
        self.book = pagelib.Book(':memory:')

        self.tags= ('xxx', 'yyy')
        self.title = 'page title'
        self.slug = 'page-title'
        self.book.new_page(
            slug  = self.slug,
            title = self.title,
            text = 'blah blah blah',
            tags = self.tags,
            )

    def test_page(self):

        self.assertEqual(
            self.title,
            self.book.page(self.slug).title
            )

    def test_update_page(self):
        p = self.book.page(self.slug)
        new_title = 'goose'
        p.title = new_title
        self.book.save(p)

        p = self.book.page(self.slug)
        self.assertEqual(
            new_title,
            p.title
            )

    def test_remove_by_slug(self):
        self.book.remove(self.slug)
        self.assertFalse( self.slug in self.book )

    def test_contains(self):
        self.assertTrue( self.slug in self.book )
        self.assertFalse( 'bogus-post' in self.book )
        self.assertFalse( None in self.book )
        self.assertFalse( 777 in self.book )

    def test_post_get(self):
        p = self.book.page(self.slug)
        self.assertEqual( p.get('title'), self.title )
        self.assertEqual(None, p.get('nothing_there') )
        self.assertEqual('shoes', p.get('nothing_there', 'shoes') )


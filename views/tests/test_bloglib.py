
import unittest
from datetime import datetime, timedelta

from . import bloglib

class TestBlogLib(unittest.TestCase):

    def setUp(self):
        self.blog = bloglib.Blog(':memory:')
        self.slug, self.post = self.blog.new_post(
            'post title',
            'blah blah blah',
            ('xxx', 'yyy'),
            )
        self.slug2, self.post2 = self.blog.new_post(
            'once more into the breach',
            'dear friends',
            ('abc', 'def',),
            )

    def test_remove(self):
        self.blog.remove_post(self.slug)
        self.assertFalse( self.slug in self.blog )

    def test_slug_creation(self):
        expected = '{}-testing-test'.format(datetime.now().year)
        slug, p = self.blog.new_post(
                    title = 'testing test',
                    content = 'test stuff'
                    )
        self.assertEqual( expected, slug )

    def test_slug_creation_in_past(self):
        expected = '2010-testing-meh'
        slug, p = self.blog.new_post(
                    title = 'testing meh',
                    content = 'more tests',
                    c_at = datetime(2010, 12, 12),
                    )
        self.assertEqual( expected, slug )

    def test_new_post(self):
        self.assertTrue( self.blog.new_post(
            title = 'a new post oh yeah',
            content = 'blah blah blah',
            c_at = datetime.now(),
            ) )

    def test_post_with_tags(self):
        slug3, post3 = self.blog.new_post(
            'yet another post',
            'walrus dude',
            ('wal', 'rus', 'xxx')
            )
        posts = self.blog.posts_with_tag('xxx')
        self.assertItemsEqual(
            [p.slug for p in posts],
            [self.post.slug, slug3]
            )

    def test_contains(self):
        self.assertTrue( self.slug in self.blog )
        self.assertFalse( 'bogus-post' in self.blog )
        self.assertFalse( None in self.blog )
        self.assertFalse( 777 in self.blog )

    def test_all(self):
        posts = self.blog.all_posts()
        # tests that all items exist and are returned in descending order of
        # creation time
        self.assertListEqual(
            [p.slug for p in posts],
            [self.slug2, self.slug],
            )

    def test_meta_list(self):
        # years,tags
        years = [datetime.now().year]
        tags =  ['xxx', 'yyy', 'abc', 'def']
        b_years, b_tags = self.blog.meta_lists()
        self.assertItemsEqual(years, b_years)
        self.assertItemsEqual(tags, b_tags)

    def test_post(self):
        self.assertEqual( self.slug, self.blog.post(self.slug).slug )

    def test_remove_post(self):
        self.blog.remove_post(self.slug)
        self.assertItemsEqual(
            [ self.slug2 ],
            [ p.slug for p in self.blog.all_posts() ]
            )

    def test_update(self):
        self.post.title = 'shock'
        self.blog.update_post(self.post)
        p = self.blog.post(self.slug)
        self.assertEqual( 'shock', p.title )

    def test_all_year(self):
        year = datetime.now().year
        self.post.c_at += timedelta(days=366)
        self.blog.update_post(self.post)
        self.assertItemsEqual(
            [ p.slug for p in self.blog.all_posts(year=year) ],
            [ self.slug2 ]
            )

    def test_post_get(self):
        self.assertTrue( self.post.get('title') )
        self.assertEqual(None, self.post.get('nothing_there') )
        self.assertEqual('shoes', self.post.get('nothing_there', 'shoes') )




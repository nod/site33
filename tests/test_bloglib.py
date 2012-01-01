
import unittest

from . import bloglib

class TestBlogLib(unittest.TestCase):

    def setUp(self):
        self.blog = bloglib.Blog(':memory:')

    def test_blog_creation(self):
        assert self.blog

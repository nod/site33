
import unittest
from bloglib import Blog, BlogPost

class TestBlogLib(unittest.TestCase):

    def setUp(self):
        self.blog = Blog(':memory:')

    def test_blog_creation(self):
        assert self.blog

import unittest
from datetime import datetime

from iso8601 import parse_date

from ..collib import DataBagCollection, DataBagMember

class CollectionLibsTests(unittest.TestCase):

    def setUp(self):
        self.c_at, self.slug= datetime.now(), 'go-slug'
        self.tags = ('x','y')
        self.dbm = DataBagMember(
            c_at=self.c_at,
            slug=self.slug,
            tags=self.tags )

    def test_base_member(self):
        self.assertEqual(self.dbm.c_at, self.c_at)
        self.assertEqual(self.dbm.slug, self.slug)
        self.assertItemsEqual(self.dbm.tags, self.tags)

    def test_d_export(self):
        self.assertDictContainsSubset(
            dict(c=self.c_at, s=self.slug, tg=self.tags),
            self.dbm._d()
            )

    def test_tags_from_db(self):
        x = DataBagMember._fd(self.dbm._d())
        self.assertItemsEqual(
            x.tags,
            self.dbm.tags
            )

    def test_datestr(self):
        d = parse_date(datetime.now().isoformat())
        self.assertIsInstance(d, datetime)
        dbm = DataBagMember( 'sluggie', c_at=d.isoformat() )
        self.assertEqual( d, dbm.c_at )

    def test_data_validation(self):

        with self.assertRaises(ValueError):
            DataBagMember('sluggie', c_at='yesterday')

        with self.assertRaises(ValueError):
            DataBagMember('sluggie', tags=23)

        dbm = DataBagMember('sluggie')
        self.assertIsInstance(
            dbm.c_at,
            datetime
            )
        self.assertTrue( hasattr(dbm.tags, '__iter__') )


class TestDBCollection(unittest.TestCase):

    def setUp(self):
        self.dbc = DataBagCollection(':memory:')

        self.slug, self.c_at = 'sluggie', datetime.now()
        self.tags = ('a', 'b')
        self.dbm = DataBagMember(self.slug, c_at=self.c_at, tags=self.tags)

    def test_save(self):
        self.dbc.save(self.dbm)
        self.assertTrue(self.dbc.member(self.slug))

    def test_in(self):
        self.dbc.save(self.dbm)
        self.assertTrue( self.dbm in self.dbc )

    def test_with_tag(self):
        self.dbc.save(self.dbm)
        self.assertTrue(
            len(self.dbc.members_with_tag('a'))
            )
        self.assertTrue(
            0 == len(self.dbc.members_with_tag('x'))
            )

    def test_all_members(self):
        self.dbc.save(self.dbm)
        self.assertTrue(
            len(self.dbc.all_members())
            )


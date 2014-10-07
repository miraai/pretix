import random

from django.test import TestCase
from django.core.cache import cache as django_cache
from django.utils.timezone import now

from tixlbase.models import Event, Organizer


class CacheTest(TestCase):
    """
    This test case tests the invalidation of the event related
    cache.
    """

    def setUp(self):
        o = Organizer.objects.create(name='Dummy', slug='dummy')
        self.event = Event.objects.create(
            organizer=o, name='Dummy', slug='dummy',
            date_from=now(),
        )
        self.cache = self.event.get_cache()
        randint = random.random()
        self.testkey = "test" + str(randint)

    def test_interference(self):
        django_cache.clear()
        self.cache.set(self.testkey, "foo")
        self.assertIsNone(django_cache.get(self.testkey))
        self.assertIn(self.cache.get(self.testkey), (None, "foo"))

    def test_longkey(self):
        self.cache.set(self.testkey * 100, "foo")
        self.assertEquals(self.cache.get(self.testkey * 100), "foo")

    def test_invalidation(self):
        self.cache.set(self.testkey, "foo")
        self.cache.clear()
        self.assertIsNone(self.cache.get(self.testkey))

    def test_many(self):
        inp = {
            'a': 'foo',
            'b': 'bar',
        }
        self.cache.set_many(inp)
        self.assertEquals(inp, self.cache.get_many(inp.keys()))
import os
import random
import string

from django.utils.timezone import utc

import factory
from factory import fuzzy
from product_details import product_details

from .models import Wine


COUNTRIES = product_details.get_regions('en').values()
YEAR_START = datetime.datetime(2000, 1, 1, tzinfo=utc)
YEAR_END = datetime.datetime(2013, 1, 1, tzinfo=utc)

# Assume there is a wine_bottle.jpn next to our tests.py
TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'wine_bottle.jpg')


def random_string(length=20):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))


class WineFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Wine

    name = factory.Sequence(lambda n: 'Wine %s' % n)
    grapes = factory.Sequence(lambda n: 'Grapes %s' % n)
    country = fuzzy.FuzzyChoice(COUNTRIES)
    region = 'RegionName'
    year = fuzzy.FuzzyDateTime(YEAR_START, YEAR_END)
    notes = factory.Sequence(lambda n: random_string())
    picture = factory.django.ImageField(from_file=TEST_IMAGE)

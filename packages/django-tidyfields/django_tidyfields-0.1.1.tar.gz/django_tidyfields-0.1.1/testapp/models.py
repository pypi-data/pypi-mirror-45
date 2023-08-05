"""
Test models required for test cases
"""

from django.db import models

from django_tidyfields.fields import TidyCharField, TidyTextField

PERMISSIVE_TIDYFIELDS = {
    'allow_tags': ['b', 'em', 'i', 'strong', 'span', 'p', 'pagebreak'],
    'safe_attrs': ['class', 'style'],
    'style': False
}


class TestModel(models.Model):
    """
    A test model to test our TidyFields against.
    """

    test_id = models.IntegerField()
    title = TidyCharField(max_length=255)
    description = TidyTextField()
    byline = TidyCharField(field_args=PERMISSIVE_TIDYFIELDS, max_length=255)
    body = TidyTextField(field_args=PERMISSIVE_TIDYFIELDS)

"""
Model fields for use on Django.db model classes
"""
from django.conf import settings
from django.db.models import CharField, TextField

from . import TIDYFIELDS_DEFAULT, tidy_input


class TidyCharField(CharField):
    """
    An enhanced CharField for sanitising input with the Python library, lxml.
    """

    def __init__(self, *args, field_args=None, **kwargs):
        """
        Initialize the TidyCharField with default arguments, and update with called parameters.

        :param field_args: (dict) optional `Cleaner` class argument overrides, format matches TIDYFIELDS defaults.
        :param args: extra args to pass to CharField __init__
        :param kwargs: undefined args
        """
        super().__init__(*args, **kwargs)

        try:
            self.kwargs = {**settings.TIDYFIELDS, **(field_args or {})}
        except AttributeError:
            self.kwargs = {**TIDYFIELDS_DEFAULT, **(field_args or {})}

    def pre_save(self, model_instance, add):
        """
        Clean text, update model and return cleaned text.

        :param model_instance: (obj) model instance
        :param add: default textfield parameter, unused
        :return: clean text as unicode
        """
        tidied = tidy_input(getattr(model_instance, self.attname), **self.kwargs)
        setattr(model_instance, self.attname, tidied)
        return tidied


class TidyTextField(TextField):
    """
    An enhanced TextField for sanitising input with the Python library, lxml.
    """

    def __init__(self, *args, field_args=None, **kwargs):
        """
        Initialize the TidyTextField with default arguments, and update with called parameters.

        :param field_args: (dict) optional `Cleaner` class argument overrides, format matches TIDYFIELDS defaults.
        :param args: extra args for passing to TextField __init__
        :param kwargs: undefined args
        """
        super().__init__(*args, **kwargs)

        try:
            self.kwargs = {**settings.TIDYFIELDS, **(field_args or {})}
        except AttributeError:
            self.kwargs = {**TIDYFIELDS_DEFAULT, **(field_args or {})}

    def pre_save(self, model_instance, add):
        """
        Clean text, update model and return cleaned text.

        :param model_instance: (obj) model instance
        :param add: default textfield parameter, unused
        :return: clean text as unicode
        """

        tidied = tidy_input(getattr(model_instance, self.attname), **self.kwargs)
        setattr(model_instance, self.attname, tidied)
        return tidied

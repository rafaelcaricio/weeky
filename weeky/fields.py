#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django import forms

from weeky.widgets import PlanningGridWidget


class MultipleChoiceGridField(forms.Field):
    widget = PlanningGridWidget
    default_error_messages = {
        'invalid_value': _(u'Enter a not empty value. The %(value)s not contains a valid value.'),
        'invalid_dict': _(u'Enter a dict of values.'),
    }

    def to_python(self, value):
        if not value:
            return {}
        elif not isinstance(value, dict):
            raise ValidationError(self.error_messages['invalid_dict'])

        dict_value = {}
        for key, val in value.items():
            dict_value[key] = smart_unicode(val)
        return dict_value

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        for key, val in value.items():
            if val in validators.EMPTY_VALUES and self.required:
                raise ValidationError(self.error_messages['invalid_value'] % {'value': key})

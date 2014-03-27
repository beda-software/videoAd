# -*- coding: utf-8 -*-
import json
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.core import exceptions, validators
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django import forms
from main.forms import PgArrayWidget

__author__ = 'lkot'


class UntypedMultipleField(forms.Field):
    def __init__(self, *args, **kwargs):
        self.coerce = kwargs.pop('coerce', lambda val: val)
        super(UntypedMultipleField, self).__init__(*args, **kwargs)


class TypedMultipleField(UntypedMultipleField):
    def to_python(self, value):
        value = super(TypedMultipleField, self).to_python(value)
        if value not in validators.EMPTY_VALUES:
            try:
                value = map(self.coerce, value)
            except (ValueError, TypeError):
                raise exceptions.ValidationError(self.error_messages['invalid'])
        return value


class TypedMultipleChoiceField(TypedMultipleField, forms.MultipleChoiceField):
    def validate(self, value):
        pass


class ArrayField(models.Field):
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return json.dumps(self.get_prep_value(value),
                          cls=DjangoJSONEncoder)

    def validate(self, value, model_instance):
        if not self.editable:
            return

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'])

        if not self.blank and value in validators.EMPTY_VALUES:
            raise exceptions.ValidationError(self.error_messages['blank'])

    def formfield(self, **kwargs):
        if self.choices:

            defaults = {
                'choices': self.choices,
                'coerce': self.coerce,
                'required': not self.blank,
                'label': capfirst(self.verbose_name),
                'help_text': self.help_text,
                'widget': forms.CheckboxSelectMultiple
            }
            defaults.update(kwargs)
            return TypedMultipleChoiceField(**defaults)
        else:
            defaults = {
                'form_class': TypedMultipleField,
                'coerce': self.coerce,
                'widget': PgArrayWidget,
            }
            defaults.update(kwargs)
            return super(ArrayField, self).formfield(**defaults)


class DateArrayField(ArrayField):
    default_error_messages = {
        'invalid': _(u'Enter only digits separated by commas.')
    }
    description = _("Array of integers")
    coerce = datetime.date

    def db_type(self, connection):
        return 'date[]'

    def to_python(self, value):
        if value == '{}':
            return []

        def strtodate(string):
            dt = datetime.datetime.strptime(string.strip(), "%Y-%m-%d")
            return datetime.date(day=dt.day, month=dt.month, year=dt.year)

        if isinstance(value, (str, unicode)):
            return map(strtodate, value.strip().split(','))

        return value

    def get_prep_value(self, value):
        return value
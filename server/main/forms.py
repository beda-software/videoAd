from StringIO import StringIO
from django import forms
from django.forms.util import flatatt
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
import unicodecsv as csv


__author__ = 'lkot'


class pgarray_dialect(csv.csv.excel):
    skipinitialspace = True


def list_to_csv(value):
    f = StringIO()
    w = csv.writer(f, pgarray_dialect)
    w.writerow(value)
    f.seek(0)
    return f.read()


class PgArrayWidget(forms.TextInput):
    class Media:
        js = (
            "/static/libs/MultiDatesPicker_v1.6.1/js/jquery-1.7.2.js",
            "/static/libs/MultiDatesPicker_v1.6.1/js/jquery.ui.core.js",
            "/static/libs/MultiDatesPicker_v1.6.1/js/jquery.ui.datepicker.js",
            "/static/libs/MultiDatesPicker_v1.6.1/jquery-ui.multidatespicker.js"
        )
        css = {
            'screen': (
                "/static/libs/MultiDatesPicker_v1.6.1/css/prettify.css",
            )
        }

    def render(self, name, value, attrs=None):

        if value is not None:
            value = list_to_csv(value)

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        attr_id = final_attrs['id']

        cdates = ''

        if value:
            final_attrs['value'] = force_text(self._format_value(value)).strip()
            cdates = ', addDates: ["%s"]' % '","'.join(final_attrs['value'].split(','))

        return mark_safe('''
            <input%s />
            <script>
                $('#%s').multiDatesPicker({dateFormat: "yy-mm-dd"%s});
            </script>''' % (flatatt(final_attrs), attr_id, cdates))

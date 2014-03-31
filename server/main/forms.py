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


class SelectWidget(forms.Select):
    def render(self, name, value, attrs=None, choices=()):

        html = super(SelectWidget, self).render(name, value, attrs, choices)

        scripts = '''
            <script>
                $(document).ready(function(){
                    $('fieldset.grp-module').eq(2).hide();

                    $('#id_partner_type').change(function(){
                        var option = $(this).find('option:selected');

                        if(option.val() == 0) {
                            $('fieldset.grp-module').eq(2).hide();
                            $('fieldset.grp-module').eq(1).show();
                        } else {
                            $('fieldset.grp-module').eq(2).show();
                            $('fieldset.grp-module').eq(1).hide();
                        }
                    });
                });
            </script>
        '''
        return mark_safe('%s%s' % (html, scripts))


class PgArrayWidget(forms.TextInput):
    class Media:
        js = (
            "/static/libs/MultiDatesPicker_v1.6.1/js/jquery-1.7.2.js",
            "/static/libs/MultiDatesPicker_v1.6.1/js/jquery.ui.core.js",
            "/static/libs/MultiDatesPicker_v1.6.1/js/jquery.ui.datepicker.js",
            "/static/libs/MultiDatesPicker_v1.6.1/jquery-ui.multidatespicker.js",
            "/static/ad_calendar.js"
        )
        css = {
            'screen': (
                "/static/libs/MultiDatesPicker_v1.6.1/css/pepper-ginder-custom.css",
            )
        }

    def render(self, name, value, attrs=None):

        if value is not None and not isinstance(value, unicode):
            value = list_to_csv(value)

        final_attrs = self.build_attrs(attrs, type='hidden', name=name)

        attr_id = final_attrs['id']
        dates = ''

        if value:
            final_attrs['value'] = force_text(self._format_value(value)).strip()
            dates = '"%s"' % '","'.join(final_attrs['value'].split(','))

        return mark_safe('''
            <div class="ad_calendar">
                <input%s data-dates='[%s]'/>
                <div style="height: 210px; width: 200px;" id="alt_%s"></div>
            </div>''' % (flatatt(final_attrs), dates, attr_id))

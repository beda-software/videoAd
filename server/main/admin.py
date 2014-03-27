from django import forms
from django.contrib import admin
from main.models import Partner, ImageAd, VideoAd, TextAd, Days, Terminal, ImidientlyAd

__author__ = 'lkot'


class DefaultAdmin(admin.ModelAdmin):
    pass


class ImidientlyAdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImidientlyAdForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].queryset = self.fields['content_type'].queryset.filter(model__in=['imagead', 'videoad', 'textad'])


class ImidientlyAdInline(admin.TabularInline):
    model = ImidientlyAd
    form = ImidientlyAdForm


class ImageAdInline(admin.TabularInline):
    model = ImageAd


class VideoAdInline(admin.TabularInline):
    model = VideoAd
    readonly_fields = ['prolongation']


class TextAdInline(admin.TabularInline):
    model = TextAd


class PartnerAdmin(admin.ModelAdmin):
    inlines = [ImageAdInline, VideoAdInline, TextAdInline]


class VideoAdminForm(forms.ModelForm):
    class Meta:
        model = VideoAd
        exclude = ['prolongation']


class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm


class DaysAdmin(admin.ModelAdmin):
    inlines = [ImidientlyAdInline, ]


admin.site.register(Partner, PartnerAdmin)
admin.site.register([ImageAd, Terminal, TextAd], DefaultAdmin)
admin.site.register(VideoAd, VideoAdmin)
admin.site.register(Days, DaysAdmin)

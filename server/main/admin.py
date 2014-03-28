from django import forms
from django.contrib import admin
from main.models import Partner, ImageAd, VideoAd, TextAd, Days, Terminal, ImmediatelyAd
from main.forms import PgArrayWidget

__author__ = 'lkot'


class DefaultAdmin(admin.ModelAdmin):
    pass


class ImmediatelyAdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImmediatelyAdForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].queryset = self.fields['content_type'].queryset.filter(model__in=['imagead', 'videoad', 'textad'])


class ImmediatelyAdInline(admin.TabularInline):
    model = ImmediatelyAd
    form = ImmediatelyAdForm


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
    inlines = [ImmediatelyAdInline, ]
    readonly_fields = ['date', 'video_ad', 'image_ad', 'text_ad', 'terminal']
    fields = ['date', 'terminal', 'video_count', 'show_text', 'text_count', 'show_video', 'start_time', 'stop_time', 'video_ad', 'image_ad', 'text_ad']
    list_display = ['date', 'terminal']
    list_filter = ['terminal', ]


admin.site.register(Partner, PartnerAdmin)
admin.site.register([ImageAd, Terminal, TextAd], DefaultAdmin)
admin.site.register(VideoAd, VideoAdmin)
admin.site.register(Days, DaysAdmin)

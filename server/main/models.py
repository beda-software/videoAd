# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import shlex
import subprocess

from django.db import models
from django.dispatch import receiver
from django.utils.html import strip_tags
from filebrowser.base import FileObject
from filebrowser.fields import FileBrowseField
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from south.modelsinspector import add_introspection_rules
from tasks import create_playlist_task, compress_video_task

from ffvideo import VideoStream
from main.fields import DateArrayField
from main.helper import PlaylistGenerator
from os import path

add_introspection_rules([], ["^main\.fields\.DateArrayField"])


PARTNER_TYPE = (
    (0, 'Физическое лицо'),
    (1, 'Юридическое лицо'),
)


class Terminal(models.Model):
    text = models.TextField('Описание')
    config = models.TextField('Конфигурация', null=True, blank=True)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'Терминал'
        verbose_name_plural = 'Терминалы'


class AdMixin(models.Model):
    terminals = models.ManyToManyField(Terminal, verbose_name='Терминалы')
    datelist = DateArrayField(verbose_name='Даты')

    class Meta:
        abstract = True


class Partner(models.Model):

    partner_type = models.PositiveIntegerField('Тип', choices=PARTNER_TYPE, default=0)

    name = models.CharField('Полное наименование', max_length=255, blank=True, null=True)
    short_name = models.CharField('Краткое наименование', max_length=500, blank=True, null=True)
    legal_address = models.CharField('Юридический адрес', max_length=400, blank=True, null=True)
    phones = models.CharField('Телефон', max_length=255, blank=True, null=True)
    director = models.CharField('Директор', max_length=255, blank=True, null=True)
    ogrn = models.CharField('ОГРН', max_length=255, blank=True, null=True)
    inn = models.CharField('ИНН', max_length=50, blank=True, null=True)
    kpp = models.CharField('КПП', max_length=50, blank=True, null=True)
    account_number = models.CharField('Номер расчетного счета', max_length=255, blank=True, null=True)
    bank = models.CharField('Банк', max_length=255, blank=True, null=True)
    bik = models.CharField('БИК', max_length=100, blank=True, null=True)
    ks = models.CharField('К/с', max_length=255, blank=True, null=True)

    full_name = models.CharField('ФИО', max_length=255, blank=True, null=True)
    passport = models.TextField('Паспортные данные с пропиской', blank=True, null=True)

    def __unicode__(self):
        return self.base_name

    @property
    def base_name(self):
        return self.name or self.short_name or self.full_name

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class VideoAd(AdMixin, models.Model):
    file_video = FileBrowseField('Видео файл', max_length=255, blank=True, null=True)
    partner = models.ForeignKey(Partner, verbose_name='Владелец объявления')
    prolongation = models.TimeField('Длительность видео', blank=True, null=True)

    def __unicode__(self):
        return '%s: %s' % (self.partner.base_name, self.file_video.filename)

    class Meta:
        verbose_name = 'Видео (объявление)'
        verbose_name_plural = 'Видео (объявления)'


class ImageAd(AdMixin, models.Model):

    image = FileBrowseField('Изображение', max_length=255)
    prolongation = models.TimeField('Длительность показа')
    partner = models.ForeignKey(Partner, verbose_name='Владелец объявления')

    def __unicode__(self):
        return '%s: %s' % (self.partner.base_name, self.image.filename)

    class Meta:
        verbose_name = 'Изображение (объявление)'
        verbose_name_plural = 'Изображение (объявления)'


class TextAd(AdMixin, models.Model):
    text = models.TextField('Содержимое объявления')
    partner = models.ForeignKey(Partner, verbose_name='Владелец объявления')

    def __unicode__(self):
        return '%s: %s' % (self.partner.base_name, strip_tags(self.text))

    class Meta:
        verbose_name = 'Текст (объявление)'
        verbose_name_plural = 'Текст (объявления)'

    @property
    def prolongation(self):
        # TODO use Django constant
        return datetime.time(minute=5)


class Days(models.Model):
    date = models.DateField('Дата')

    video_ad = models.ManyToManyField(VideoAd, verbose_name='Видео', blank=True, null=True)
    image_ad = models.ManyToManyField(ImageAd, verbose_name='Изображение', blank=True, null=True)
    text_ad = models.ManyToManyField(TextAd, verbose_name='Тексты', blank=True, null=True)

    video_count = models.PositiveIntegerField('Количество показов видео', default=0)
    show_text = models.BooleanField('Показывать текст в блоке видео')

    text_count = models.PositiveIntegerField('Количество показов текста', default=0)
    show_video = models.BooleanField('Показывать видео в блоке текст')

    start_time = models.TimeField('Время начала показа', default=datetime.time(hour=8))
    stop_time = models.TimeField('Время остановки показа', default=datetime.time(hour=22))

    terminal = models.ForeignKey(Terminal, verbose_name='Терминал')

    def __unicode__(self):
        return unicode(self.date)

    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'


class ImmediatelyAd(models.Model):
    day = models.ForeignKey(Days, verbose_name='День', related_name='immediatelies')
    time = models.TimeField('Время показа')

    content_type = models.ForeignKey(ContentType, verbose_name='Тип объявления')
    object_id = models.PositiveIntegerField('ID объявления')
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'


class OsCommandLog(models.Model):
    command = models.TextField('Текст комманды')
    ouput = models.TextField('STDOUT')
    errors = models.TextField('STDERR')
    return_code = models.CharField('Код выполнения', max_length=255)
    datetime = models.DateTimeField('Дата выполнения', auto_now=True)

    def __unicode__(self):
        return self.command

    class Meta:
        verbose_name = 'Лог выполнения комманд'
        verbose_name_plural = 'Логи выполнения комманд'


@receiver(pre_save, sender=VideoAd)
def set_duration_video(sender, instance, **kwargs):
    if instance.file_video:
        video_stream = VideoStream(instance.file_video.path_full)
        seconds=int(video_stream.duration)
        instance.prolongation = datetime.time(hour=seconds/3600, minute=seconds/60, second=seconds%60)


def create_update_day(sender, instance, **kwargs):

    if kwargs['action'] != 'post_add':
        return

    model, field = instance._meta.model, ''

    if model == VideoAd:
        field = 'video_ad'

        # test to compress
        if not '_compress' in instance.file_video.filename:
            return

    elif model == TextAd:
        field = 'text_ad'
    elif model == ImageAd:
        field = 'image_ad'

    if field == '':
        return

    for terminal in instance.terminals.all():
        for date in instance.datelist:

            try:
                day = Days.objects.get(date=date, terminal_id=terminal.pk)
            except Days.DoesNotExist:
                day = Days(date=date,
                           terminal=terminal,
                           show_text=True,
                           show_video=True,
                           start_time=datetime.time(hour=8),
                           stop_time=datetime.time(hour=20))

                day.save()

            getattr(day, field).add(instance)
            day.save()


# not used
def create_playlist(sender, instance, **kwargs):
    if 'action' in kwargs and kwargs['action'] != 'post_add':
        return

    create_playlist_task.delay(day=instance)


def compress_video(sender, instance, **kwargs):
    compress_video_task.delay(video=instance)


# Day update
m2m_changed.connect(create_update_day, sender=VideoAd.terminals.through)
m2m_changed.connect(create_update_day, sender=TextAd.terminals.through)
m2m_changed.connect(create_update_day, sender=ImageAd.terminals.through)

# Compress video signal
post_save.connect(compress_video, sender=VideoAd)

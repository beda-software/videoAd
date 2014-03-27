# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.dispatch import receiver
from django.utils.html import strip_tags
from filebrowser.fields import FileBrowseField
from django.db.models.signals import pre_save
from ffvideo import VideoStream
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Partner(models.Model):
    name = models.CharField('Наименование организации', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class VideoAd(models.Model):
    file_video = FileBrowseField('Видео файл', max_length=255, blank=True, null=True)
    partner = models.ForeignKey(Partner, verbose_name='Владелец объявления')
    prolongation = models.TimeField('Длительность видео', blank=True, null=True)

    def __unicode__(self):
        return '%s: %s' % (self.partner.name, self.file_video)

    class Meta:
        verbose_name = 'Видео (объявление)'
        verbose_name_plural = 'Видео (объявления)'


class ImageAd(models.Model):

    def image_file(self, filename):
        return '/'.join([datetime.datetime.now().strftime('image/%Y/%m/%d'), filename])

    image = models.ImageField('Изображение', upload_to=image_file)
    prolongation = models.TimeField('Длительность показа')
    partner = models.ForeignKey(Partner, verbose_name='Владелец объявления')

    def __unicode__(self):
        return '%s: %s' % (self.partner.name, self.image.name.split('/')[-1])

    class Meta:
        verbose_name = 'Изображение (объявление)'
        verbose_name_plural = 'Изображение (объявления)'


class TextAd(models.Model):
    text = models.TextField('Содержимое объявления')
    partner = models.ForeignKey(Partner, verbose_name='Владелец объявления')

    def __unicode__(self):
        return '%s: %s' % (self.partner.name, strip_tags(self.text))

    class Meta:
        verbose_name = 'Текст (объявление)'
        verbose_name_plural = 'Текст (объявления)'


class Terminal(models.Model):
    text = models.TextField('Описание')
    config = models.TextField('Конфигурация')

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'Терминал'
        verbose_name_plural = 'Терминалы'


class Days(models.Model):
    date = models.DateField('Дата')

    video_ad = models.ManyToManyField(VideoAd, verbose_name='Видео', blank=True, null=True)
    image_ad = models.ManyToManyField(ImageAd, verbose_name='Изображение', blank=True, null=True)
    text_ad = models.ManyToManyField(TextAd, verbose_name='Тексты', blank=True, null=True)

    time_for_video = models.TimeField('Интервал показа видео')
    show_text = models.BooleanField('Показывать текст в блоке видео')

    time_for_text = models.TimeField('Интервал показа текста')
    show_video = models.BooleanField('Показывать видео в блоке текст')

    start_time = models.TimeField('Время начала показа')
    stop_time = models.TimeField('Время остановки показа')

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


@receiver(pre_save, sender=VideoAd)
def set_duration_video(sender, instance, **kwargs):
    if instance.file_video:
        video_stream = VideoStream(instance.file_video.path_full)
        seconds=int(video_stream.duration)
        instance.prolongation = datetime.time(hour=seconds/3600, minute=seconds/60, second=seconds%60)
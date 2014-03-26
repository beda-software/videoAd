# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VideoAd.prolongation'
        db.add_column(u'main_videoad', 'prolongation',
                      self.gf('django.db.models.fields.TimeField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'VideoAd.file_video'
        db.alter_column(u'main_videoad', 'file_video', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, null=True))
        # Adding field 'ImageAd.prolongation'
        db.add_column(u'main_imagead', 'prolongation',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.timedelta(0)),
                      keep_default=False)


        # Changing field 'ImageAd.image'
        db.alter_column(u'main_imagead', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    def backwards(self, orm):
        # Deleting field 'VideoAd.prolongation'
        db.delete_column(u'main_videoad', 'prolongation')


        # Changing field 'VideoAd.file_video'
        db.alter_column(u'main_videoad', 'file_video', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))
        # Deleting field 'ImageAd.prolongation'
        db.delete_column(u'main_imagead', 'prolongation')


        # Changing field 'ImageAd.image'
        db.alter_column(u'main_imagead', 'image', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    models = {
        u'main.days': {
            'Meta': {'object_name': 'Days'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_ad': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.ImageAd']", 'symmetrical': 'False'}),
            'show_text': ('django.db.models.fields.BooleanField', [], {}),
            'show_video': ('django.db.models.fields.BooleanField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'stop_time': ('django.db.models.fields.TimeField', [], {}),
            'terminal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Terminal']"}),
            'text_ad': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.TextAd']", 'symmetrical': 'False'}),
            'time_for_text': ('django.db.models.fields.TimeField', [], {}),
            'time_for_video': ('django.db.models.fields.TimeField', [], {}),
            'video_ad': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.VideoAd']", 'symmetrical': 'False'})
        },
        u'main.imagead': {
            'Meta': {'object_name': 'ImageAd'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'prolongation': ('django.db.models.fields.TimeField', [], {})
        },
        u'main.partner': {
            'Meta': {'object_name': 'Partner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.terminal': {
            'Meta': {'object_name': 'Terminal'},
            'config': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'main.textad': {
            'Meta': {'object_name': 'TextAd'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'main.videoad': {
            'Meta': {'object_name': 'VideoAd'},
            'file_video': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'prolongation': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'youtube_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['main']
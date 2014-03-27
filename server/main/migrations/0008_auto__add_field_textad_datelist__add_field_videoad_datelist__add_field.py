# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TextAd.datelist'
        db.add_column(u'main_textad', 'datelist',
                      self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype=u'date', null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoAd.datelist'
        db.add_column(u'main_videoad', 'datelist',
                      self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype=u'date', null=True, blank=True),
                      keep_default=False)

        # Adding field 'ImageAd.datelist'
        db.add_column(u'main_imagead', 'datelist',
                      self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype=u'date', null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TextAd.datelist'
        db.delete_column(u'main_textad', 'datelist')

        # Deleting field 'VideoAd.datelist'
        db.delete_column(u'main_videoad', 'datelist')

        # Deleting field 'ImageAd.datelist'
        db.delete_column(u'main_imagead', 'datelist')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.days': {
            'Meta': {'object_name': 'Days'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_ad': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.ImageAd']", 'null': 'True', 'blank': 'True'}),
            'show_text': ('django.db.models.fields.BooleanField', [], {}),
            'show_video': ('django.db.models.fields.BooleanField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'stop_time': ('django.db.models.fields.TimeField', [], {}),
            'terminal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Terminal']"}),
            'text_ad': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.TextAd']", 'null': 'True', 'blank': 'True'}),
            'time_for_text': ('django.db.models.fields.TimeField', [], {}),
            'time_for_video': ('django.db.models.fields.TimeField', [], {}),
            'video_ad': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.VideoAd']", 'null': 'True', 'blank': 'True'})
        },
        u'main.imagead': {
            'Meta': {'object_name': 'ImageAd'},
            'datelist': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "u'date'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'prolongation': ('django.db.models.fields.TimeField', [], {}),
            'terminals': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Terminal']", 'symmetrical': 'False'})
        },
        u'main.immediatelyad': {
            'Meta': {'object_name': 'ImmediatelyAd'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'immediatelies'", 'to': u"orm['main.Days']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.TimeField', [], {})
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
            'datelist': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "u'date'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'terminals': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Terminal']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'main.videoad': {
            'Meta': {'object_name': 'VideoAd'},
            'datelist': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "u'date'", 'null': 'True', 'blank': 'True'}),
            'file_video': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'prolongation': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'terminals': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Terminal']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['main']
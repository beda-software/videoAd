# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Partner.partner_type'
        db.add_column(u'main_partner', 'partner_type',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Partner.short_name'
        db.add_column(u'main_partner', 'short_name',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.legal_address'
        db.add_column(u'main_partner', 'legal_address',
                      self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.phones'
        db.add_column(u'main_partner', 'phones',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.director'
        db.add_column(u'main_partner', 'director',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.ogrn'
        db.add_column(u'main_partner', 'ogrn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.inn'
        db.add_column(u'main_partner', 'inn',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.kpp'
        db.add_column(u'main_partner', 'kpp',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.account_number'
        db.add_column(u'main_partner', 'account_number',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.bank'
        db.add_column(u'main_partner', 'bank',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.bik'
        db.add_column(u'main_partner', 'bik',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.ks'
        db.add_column(u'main_partner', 'ks',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.full_name'
        db.add_column(u'main_partner', 'full_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partner.passport'
        db.add_column(u'main_partner', 'passport',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Partner.name'
        db.alter_column(u'main_partner', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):
        # Deleting field 'Partner.partner_type'
        db.delete_column(u'main_partner', 'partner_type')

        # Deleting field 'Partner.short_name'
        db.delete_column(u'main_partner', 'short_name')

        # Deleting field 'Partner.legal_address'
        db.delete_column(u'main_partner', 'legal_address')

        # Deleting field 'Partner.phones'
        db.delete_column(u'main_partner', 'phones')

        # Deleting field 'Partner.director'
        db.delete_column(u'main_partner', 'director')

        # Deleting field 'Partner.ogrn'
        db.delete_column(u'main_partner', 'ogrn')

        # Deleting field 'Partner.inn'
        db.delete_column(u'main_partner', 'inn')

        # Deleting field 'Partner.kpp'
        db.delete_column(u'main_partner', 'kpp')

        # Deleting field 'Partner.account_number'
        db.delete_column(u'main_partner', 'account_number')

        # Deleting field 'Partner.bank'
        db.delete_column(u'main_partner', 'bank')

        # Deleting field 'Partner.bik'
        db.delete_column(u'main_partner', 'bik')

        # Deleting field 'Partner.ks'
        db.delete_column(u'main_partner', 'ks')

        # Deleting field 'Partner.full_name'
        db.delete_column(u'main_partner', 'full_name')

        # Deleting field 'Partner.passport'
        db.delete_column(u'main_partner', 'passport')


        # Changing field 'Partner.name'
        db.alter_column(u'main_partner', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

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
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(8, 0)'}),
            'stop_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(22, 0)'}),
            'terminal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Terminal']"}),
            'text_ad': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.TextAd']", 'null': 'True', 'blank': 'True'}),
            'text_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'video_ad': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.VideoAd']", 'null': 'True', 'blank': 'True'}),
            'video_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'main.imagead': {
            'Meta': {'object_name': 'ImageAd'},
            'datelist': ('main.fields.DateArrayField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255'}),
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
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bik': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'kpp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'ks': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'legal_address': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ogrn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'partner_type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'passport': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phones': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'main.terminal': {
            'Meta': {'object_name': 'Terminal'},
            'config': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'main.textad': {
            'Meta': {'object_name': 'TextAd'},
            'datelist': ('main.fields.DateArrayField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'terminals': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Terminal']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'main.videoad': {
            'Meta': {'object_name': 'VideoAd'},
            'datelist': ('main.fields.DateArrayField', [], {}),
            'file_video': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'prolongation': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'terminals': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Terminal']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['main']
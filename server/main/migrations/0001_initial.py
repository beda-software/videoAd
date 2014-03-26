# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Partner'
        db.create_table(u'main_partner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'main', ['Partner'])

        # Adding model 'VideoAd'
        db.create_table(u'main_videoad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('youtube_code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('file_video', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Partner'])),
        ))
        db.send_create_signal(u'main', ['VideoAd'])

        # Adding model 'ImageAd'
        db.create_table(u'main_imagead', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Partner'])),
        ))
        db.send_create_signal(u'main', ['ImageAd'])

        # Adding model 'TextAd'
        db.create_table(u'main_textad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Partner'])),
        ))
        db.send_create_signal(u'main', ['TextAd'])

        # Adding model 'Terminal'
        db.create_table(u'main_terminal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('config', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['Terminal'])

        # Adding model 'Days'
        db.create_table(u'main_days', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time_for_video', self.gf('django.db.models.fields.TimeField')()),
            ('show_text', self.gf('django.db.models.fields.BooleanField')()),
            ('time_for_text', self.gf('django.db.models.fields.TimeField')()),
            ('show_video', self.gf('django.db.models.fields.BooleanField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('stop_time', self.gf('django.db.models.fields.TimeField')()),
            ('terminal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Terminal'])),
        ))
        db.send_create_signal(u'main', ['Days'])

        # Adding M2M table for field video_ad on 'Days'
        m2m_table_name = db.shorten_name(u'main_days_video_ad')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('days', models.ForeignKey(orm[u'main.days'], null=False)),
            ('videoad', models.ForeignKey(orm[u'main.videoad'], null=False))
        ))
        db.create_unique(m2m_table_name, ['days_id', 'videoad_id'])

        # Adding M2M table for field image_ad on 'Days'
        m2m_table_name = db.shorten_name(u'main_days_image_ad')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('days', models.ForeignKey(orm[u'main.days'], null=False)),
            ('imagead', models.ForeignKey(orm[u'main.imagead'], null=False))
        ))
        db.create_unique(m2m_table_name, ['days_id', 'imagead_id'])

        # Adding M2M table for field text_ad on 'Days'
        m2m_table_name = db.shorten_name(u'main_days_text_ad')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('days', models.ForeignKey(orm[u'main.days'], null=False)),
            ('textad', models.ForeignKey(orm[u'main.textad'], null=False))
        ))
        db.create_unique(m2m_table_name, ['days_id', 'textad_id'])


    def backwards(self, orm):
        # Deleting model 'Partner'
        db.delete_table(u'main_partner')

        # Deleting model 'VideoAd'
        db.delete_table(u'main_videoad')

        # Deleting model 'ImageAd'
        db.delete_table(u'main_imagead')

        # Deleting model 'TextAd'
        db.delete_table(u'main_textad')

        # Deleting model 'Terminal'
        db.delete_table(u'main_terminal')

        # Deleting model 'Days'
        db.delete_table(u'main_days')

        # Removing M2M table for field video_ad on 'Days'
        db.delete_table(db.shorten_name(u'main_days_video_ad'))

        # Removing M2M table for field image_ad on 'Days'
        db.delete_table(db.shorten_name(u'main_days_image_ad'))

        # Removing M2M table for field text_ad on 'Days'
        db.delete_table(db.shorten_name(u'main_days_text_ad'))


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
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"})
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
            'file_video': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Partner']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'youtube_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['main']
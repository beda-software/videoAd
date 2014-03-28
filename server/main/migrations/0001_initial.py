# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Terminal'
        db.create_table(u'main_terminal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('config', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['Terminal'])

        # Adding model 'Partner'
        db.create_table(u'main_partner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'main', ['Partner'])

        # Adding model 'VideoAd'
        db.create_table(u'main_videoad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datelist', self.gf('main.fields.DateArrayField')()),
            ('file_video', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, null=True, blank=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Partner'])),
            ('prolongation', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['VideoAd'])

        # Adding M2M table for field terminals on 'VideoAd'
        m2m_table_name = db.shorten_name(u'main_videoad_terminals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videoad', models.ForeignKey(orm[u'main.videoad'], null=False)),
            ('terminal', models.ForeignKey(orm[u'main.terminal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videoad_id', 'terminal_id'])

        # Adding model 'ImageAd'
        db.create_table(u'main_imagead', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datelist', self.gf('main.fields.DateArrayField')()),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=255)),
            ('prolongation', self.gf('django.db.models.fields.TimeField')()),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Partner'])),
        ))
        db.send_create_signal(u'main', ['ImageAd'])

        # Adding M2M table for field terminals on 'ImageAd'
        m2m_table_name = db.shorten_name(u'main_imagead_terminals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('imagead', models.ForeignKey(orm[u'main.imagead'], null=False)),
            ('terminal', models.ForeignKey(orm[u'main.terminal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['imagead_id', 'terminal_id'])

        # Adding model 'TextAd'
        db.create_table(u'main_textad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datelist', self.gf('main.fields.DateArrayField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Partner'])),
        ))
        db.send_create_signal(u'main', ['TextAd'])

        # Adding M2M table for field terminals on 'TextAd'
        m2m_table_name = db.shorten_name(u'main_textad_terminals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('textad', models.ForeignKey(orm[u'main.textad'], null=False)),
            ('terminal', models.ForeignKey(orm[u'main.terminal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['textad_id', 'terminal_id'])

        # Adding model 'Days'
        db.create_table(u'main_days', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time_for_video', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('show_text', self.gf('django.db.models.fields.BooleanField')()),
            ('time_for_text', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('show_video', self.gf('django.db.models.fields.BooleanField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(8, 0))),
            ('stop_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(22, 0))),
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

        # Adding model 'ImmediatelyAd'
        db.create_table(u'main_immediatelyad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'immediatelies', to=orm['main.Days'])),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'main', ['ImmediatelyAd'])


    def backwards(self, orm):
        # Deleting model 'Terminal'
        db.delete_table(u'main_terminal')

        # Deleting model 'Partner'
        db.delete_table(u'main_partner')

        # Deleting model 'VideoAd'
        db.delete_table(u'main_videoad')

        # Removing M2M table for field terminals on 'VideoAd'
        db.delete_table(db.shorten_name(u'main_videoad_terminals'))

        # Deleting model 'ImageAd'
        db.delete_table(u'main_imagead')

        # Removing M2M table for field terminals on 'ImageAd'
        db.delete_table(db.shorten_name(u'main_imagead_terminals'))

        # Deleting model 'TextAd'
        db.delete_table(u'main_textad')

        # Removing M2M table for field terminals on 'TextAd'
        db.delete_table(db.shorten_name(u'main_textad_terminals'))

        # Deleting model 'Days'
        db.delete_table(u'main_days')

        # Removing M2M table for field video_ad on 'Days'
        db.delete_table(db.shorten_name(u'main_days_video_ad'))

        # Removing M2M table for field image_ad on 'Days'
        db.delete_table(db.shorten_name(u'main_days_image_ad'))

        # Removing M2M table for field text_ad on 'Days'
        db.delete_table(db.shorten_name(u'main_days_text_ad'))

        # Deleting model 'ImmediatelyAd'
        db.delete_table(u'main_immediatelyad')


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
            'time_for_text': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'time_for_video': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'video_ad': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.VideoAd']", 'null': 'True', 'blank': 'True'})
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
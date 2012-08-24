# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tumblelog'
        db.create_table('tumbledore_tumblelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('mount_on', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=200, db_index=True, blank=True)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('posts_per_page', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('extra_styles', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('extra_scripts', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tumbledore', ['Tumblelog'])

        # Adding model 'TumblelogPost'
        db.create_table('tumbledore_tumblelogpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ('tumblelog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['tumbledore.Tumblelog'])),
            ('author', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('excerpt', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_permalink', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('tumbledore', ['TumblelogPost'])

        # Adding unique constraint on 'TumblelogPost', fields ['slug', 'tumblelog']
        db.create_unique('tumbledore_tumblelogpost', ['slug', 'tumblelog_id'])

        # Adding model 'TumblelogWidget'
        db.create_table('tumbledore_tumblelogwidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tumbledore', ['TumblelogWidget'])

        # Adding model 'TumblelogWidgetPlacement'
        db.create_table('tumbledore_tumblelogwidgetplacement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tumblelog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='placement_set', to=orm['tumbledore.Tumblelog'])),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(related_name='placement_set', to=orm['tumbledore.TumblelogWidget'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('tumbledore', ['TumblelogWidgetPlacement'])


    def backwards(self, orm):
        # Removing unique constraint on 'TumblelogPost', fields ['slug', 'tumblelog']
        db.delete_unique('tumbledore_tumblelogpost', ['slug', 'tumblelog_id'])

        # Deleting model 'Tumblelog'
        db.delete_table('tumbledore_tumblelog')

        # Deleting model 'TumblelogPost'
        db.delete_table('tumbledore_tumblelogpost')

        # Deleting model 'TumblelogWidget'
        db.delete_table('tumbledore_tumblelogwidget')

        # Deleting model 'TumblelogWidgetPlacement'
        db.delete_table('tumbledore_tumblelogwidgetplacement')


    models = {
        'tumbledore.tumblelog': {
            'Meta': {'object_name': 'Tumblelog'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'extra_scripts': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'extra_styles': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mount_on': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '200', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'posts_per_page': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'widgets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tumbledore.TumblelogWidget']", 'through': "orm['tumbledore.TumblelogWidgetPlacement']", 'symmetrical': 'False'})
        },
        'tumbledore.tumblelogpost': {
            'Meta': {'ordering': "('-is_sticky', '-published_at')", 'unique_together': "(('slug', 'tumblelog'),)", 'object_name': 'TumblelogPost'},
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'has_permalink': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tumblelog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['tumbledore.Tumblelog']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tumbledore.tumblelogwidget': {
            'Meta': {'object_name': 'TumblelogWidget'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tumbledore.tumblelogwidgetplacement': {
            'Meta': {'ordering': "('order',)", 'object_name': 'TumblelogWidgetPlacement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tumblelog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'placement_set'", 'to': "orm['tumbledore.Tumblelog']"}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'placement_set'", 'to': "orm['tumbledore.TumblelogWidget']"})
        }
    }

    complete_apps = ['tumbledore']
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.utils.timezone
import mptt.fields
import cms.models.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '__latest__'),
        ('filer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text='Is this object active?', verbose_name='Active')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='children', verbose_name='Parent', blank=True, to='blogit.Category', null=True)),
            ],
            options={
                'db_table': 'blogit_categories',
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='translations', editable=False, to='blogit.Category', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'blogit_categories_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'Category Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('status', models.IntegerField(default=0, help_text='When draft post is visible to staff only, when private to author only, and when public to everyone.', verbose_name='Status', choices=[(0, 'Draft'), (1, 'Private'), (2, 'Public'), (3, 'Hidden')])),
                ('date_published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Published on')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('body', cms.models.fields.PlaceholderField(related_name='post_body_set', slotname='blogit_post_body', editable=False, to='cms.Placeholder', null=True)),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Category', blank=True, to='blogit.Category', null=True)),
                ('featured_image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Featured Image', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'ordering': ('-date_published',),
                'db_table': 'blogit_posts',
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'get_latest_by': 'date_published',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('meta_title', models.CharField(max_length=255, verbose_name='Meta title', blank=True)),
                ('meta_description', models.TextField(help_text='The text displayed in search engines.', max_length=155, verbose_name='Meta description', blank=True)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='translations', editable=False, to='blogit.Post', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'blogit_posts_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'Post Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text='Is this object active?', verbose_name='Active')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
            ],
            options={
                'db_table': 'blogit_tags',
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, related_name='translations', editable=False, to='blogit.Tag', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'blogit_tags_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'Tag Translation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tagtranslation',
            unique_together=set([('language_code', 'master'), ('slug', 'language_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='posttranslation',
            unique_together=set([('language_code', 'master'), ('slug', 'language_code')]),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='tagged_posts', null=True, verbose_name='Tags', to='blogit.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('language_code', 'master'), ('slug', 'language_code')]),
        ),
    ]

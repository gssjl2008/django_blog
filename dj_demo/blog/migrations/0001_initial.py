# Generated by Django 3.0.6 on 2020-05-21 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='article category')),
            ],
            options={
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='article tag')),
            ],
            options={
                'verbose_name': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_created=True, verbose_name='create time')),
                ('phone', models.CharField(max_length=20, verbose_name='phone number')),
                ('author_name', models.OneToOneField(max_length=50, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Author',
                'ordering': ['create_time'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_created=True, verbose_name='article create time')),
                ('title', models.CharField(max_length=100, verbose_name='article title')),
                ('sub_title', models.CharField(blank=True, max_length=140, verbose_name='article sub title')),
                ('overview', models.CharField(blank=True, max_length=200, verbose_name='article overview')),
                ('text', models.TextField(verbose_name='article body')),
                ('modity_time', models.DateTimeField(auto_now_add=True, verbose_name='article modity time')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='blog.Category')),
                ('tag', models.ManyToManyField(blank=True, related_name='tags', to='blog.Tag')),
            ],
            options={
                'verbose_name': 'Article',
                'ordering': ['create_time'],
            },
        ),
    ]

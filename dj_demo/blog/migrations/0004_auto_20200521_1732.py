# Generated by Django 3.0.6 on 2020-05-21 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_menu_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='rank',
            field=models.IntegerField(auto_created=True, unique=True, verbose_name='name rank'),
        ),
    ]
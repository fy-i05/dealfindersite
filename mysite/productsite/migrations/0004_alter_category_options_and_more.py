# Generated by Django 5.1 on 2024-09-03 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productsite', '0003_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set(),
        ),
    ]

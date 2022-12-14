# Generated by Django 3.1.7 on 2021-04-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210429_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variables',
            name='apology_msg_en',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='variables',
            name='apology_msg_fr',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='variables',
            name='default_fallback_msg_en',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='variables',
            name='default_fallback_msg_fr',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='variables',
            name='greeting_msg_en',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='variables',
            name='greeting_msg_fr',
            field=models.TextField(default=''),
        ),
    ]

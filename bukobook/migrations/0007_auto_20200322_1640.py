# Generated by Django 3.0.3 on 2020-03-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bukobook', '0006_comment_reply_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='floor',
            field=models.IntegerField(default=0),
        ),
    ]

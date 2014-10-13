# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141010_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=sorl.thumbnail.fields.ImageField(default=b'profile_pics/defaultIcon.png', null=True, upload_to=b'profile_pics', blank=True),
        ),
    ]

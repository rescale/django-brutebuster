# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BruteBuster', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failedattempt',
            name='IP',
            field=models.GenericIPAddressField(null=True, verbose_name=b'IP Address'),
        ),
    ]

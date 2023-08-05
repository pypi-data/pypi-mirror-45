# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-15 21:45
from __future__ import unicode_literals

from django.db import migrations


def populate_default_group(apps, schema_editor):
    from tendenci.apps.user_groups.utils import get_default_group
    try:
        group_id = get_default_group()
        File = apps.get_model("files", "File")
        File.objects.filter(group=None).update(group_id=group_id)
    except:
        pass  


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_auto_20180724_1745'),
        ('user_groups', '0002_group_show_for_memberships'),
    ]

    operations = [
        migrations.RunPython(populate_default_group),
    ]

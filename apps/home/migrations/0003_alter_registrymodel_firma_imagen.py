# Generated by Django 3.2.6 on 2024-12-15 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_registrymodel_firma_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrymodel',
            name='firma_imagen',
            field=models.CharField(max_length=400),
        ),
    ]
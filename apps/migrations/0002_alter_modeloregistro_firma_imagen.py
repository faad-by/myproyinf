# Generated by Django 3.2.6 on 2024-12-16 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modeloregistro',
            name='firma_imagen',
            field=models.CharField(max_length=1200),
        ),
    ]

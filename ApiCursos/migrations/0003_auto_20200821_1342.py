# Generated by Django 2.1.5 on 2020-08-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiCursos', '0002_auto_20200815_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='estado',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='profesor',
            name='estado',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='estado',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]

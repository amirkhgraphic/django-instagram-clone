# Generated by Django 4.2.10 on 2024-03-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_storymention_postmention'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmedia',
            name='type',
            field=models.CharField(blank=True, choices=[('IMAGE', 'image'), ('VIDEO', 'video')], max_length=5, null=True),
        ),
    ]

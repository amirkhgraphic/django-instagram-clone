# Generated by Django 4.2.10 on 2024-03-04 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_storymention_postmention'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_activity', '0002_postlike_delete_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_likes', to='content.story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

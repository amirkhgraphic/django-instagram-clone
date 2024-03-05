import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class GalleryMixin(models.Model):
    TYPES = (
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('AUDIO', 'Audio'),
    )

    VIDEO = (
        ('MP4', 'mp4'),
        ('AVI', 'avi'),
        ('MKV', 'mkv'),
        ('MOV', 'mov'),
        ('WMV', 'wmv'),
        ('FLV', 'flv'),
        ('WebM', 'webm'),
    )

    IMAGE = (
        ('JPEG', 'jpeg'),
        ('JPG', 'jpg'),
        ('PNG', 'png'),
        ('GIF', 'gif'),
        ('BMP', 'bmp'),
        ('SVG', 'svg'),
        ('WebP', 'webp'),
        ('TIFF', 'tiff'),
    )

    AUDIO = (
        ('MP3', 'mp3'),
        ('WAV', 'wav'),
        ('AAC', 'aac'),
        ('FLAC', 'flac'),
        ('OGG', 'ogg'),
        ('M4A', 'm4a'),
        ('AIFF', 'aiff'),
    )

    FORMATS = IMAGE + VIDEO + AUDIO

    file = None  # NotImplementedError('where is your file going to be uploaded to you genius? :|')
    format = models.CharField(max_length=5, choices=FORMATS, editable=False)
    type = models.CharField(max_length=5, choices=TYPES, editable=False)

    @property
    def html_tag(self):
        if self.type == 'IMAGE':
            return format_html(
                f'<img class="media" src="{self.file.url}" alt={self.file.name}/>'
            )
        elif self.type == 'VIDEO':
            return format_html(
                f'<video class="media" controls><source src="{self.file.url}" '
                f'type="video/{self.format.lower()}">Your browser does not support the video tag.</video>'
            )
        elif self.type == 'AUDIO':
            return format_html(
                f'<audio class="media" controls><source src="{self.file.url}" type="audio/{self.format.lower()}">Your browser does not '
                f'support the audio element.</audio>',
            )
        else:
            return "Unsupported Format"

    @classmethod
    def get_images(cls):
        return cls.objects.filter(file_type='IMAGE')

    @classmethod
    def get_videos(cls):
        return cls.objects.filter(file_type='VIDEO')

    @classmethod
    def get_audios(cls):
        return cls.objects.filter(file_type='AUDIO')

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.file:
            file_extension: str = self.file.name.split('.')[-1].lower()

            if file_extension in dict(GalleryMixin.IMAGE).values():
                self.format = file_extension.upper()
                self.type = 'IMAGE'

            elif file_extension in dict(GalleryMixin.VIDEO).values():
                self.format = file_extension.upper()
                self.type = 'VIDEO'

            elif file_extension in dict(GalleryMixin.AUDIO).values():
                self.format = file_extension.upper()
                self.type = 'AUDIO'

            else:
                raise ValidationError('UNSUPPORTED FORMAT')

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.file.name.split("/")[-1]}'

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
        abstract = True


class CategoryMixin(models.Model):
    name = models.CharField(max_length=127, unique=True)
    thumbnail = None

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        abstract = True

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.thumbnail and ('default' not in self.thumbnail.name):
            if os.path.isfile(self.thumbnail.path):
                os.remove(self.thumbnail.path)

        super().delete(*args, **kwargs)
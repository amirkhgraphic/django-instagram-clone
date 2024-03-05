from django.db import models


class Log(models.Model):
    OPERATION_TYPES = (
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('WRITE', 'Write'),
        ('DELETE', 'Delete'),
        ('UPDATE', 'Update'),
    )

    action = models.TextField()
    operation = models.CharField(choices=OPERATION_TYPES, max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

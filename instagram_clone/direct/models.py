from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def time_diff(self):
        diff = timezone.now() - self.created_at
        seconds = diff.seconds
        h = seconds // (60 * 60)
        m = (seconds - h * 60 * 60) // 60
        s = seconds - (h * 60 * 60) - (m * 60)

        if diff.days:
            return f"{diff.days} days ago"
        if h != 0:
            if h == 1:
                return f"{m} hour ago"
            return f"{h} hours ago"
        elif m != 0:
            if m == 1:
                return f"{m} minute ago"
            return f"{m} minutes ago"
        else:
            return f"{s} seconds ago"

    def __str__(self):
        return f"From {self.sender.user_name} to {self.receiver.user_name}: ({self.time_diff})"

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from content.models import Post, Story, PostMedia

User = get_user_model()


class Comment(models.Model):
    content = models.CharField(max_length=200, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def post_comments(cls, pk):
        return cls.objects.filter(post_id=pk)

    @property
    def time_diff(self):
        diff = timezone.now() - self.created_at
        seconds = diff.seconds
        h = seconds//(60*60)
        m = (seconds-h*60*60)//60
        s = seconds-(h*60*60)-(m*60)

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
        return f"Comment on {self.post}"

    class Meta:
        ordering = ['-created_at']


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def post_likes(cls, pk):
        return cls.objects.filter(post_id=pk)

    def __str__(self):
        return f"Liked {self.post}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'post')


class StoryLike(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def story_likes(cls, pk):
        return cls.objects.filter(story_id=pk)

    def __str__(self):
        return f"Liked {self.story}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'story')

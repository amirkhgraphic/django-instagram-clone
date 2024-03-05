from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(null=True, blank=True)
    comment_is_allowed = models.BooleanField(default=True)
    likes_count_display = models.BooleanField(default=True)
    close_friends_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def no_of_media(self):
        return PostMedia.objects.filter(post=self).count()

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
        return f"Post of {self.user.user_name}"

    class Meta:
        ordering = ['-created_at']


class Story(models.Model):
    TYPES = (
        ('IMAGE', 'image'),
        ('VIDEO', 'video')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    caption = models.TextField(null=True, blank=True)
    media = models.FileField(upload_to='story/')
    media_type = models.CharField(choices=TYPES, max_length=5)
    likes_count_display = models.BooleanField(default=True)
    close_friends_only = models.BooleanField(default=False)
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
        return f"Story of {self.user.user_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'


# recent_stories = Story.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(hours=24))


class PostMedia(models.Model):
    TYPES = (
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video')
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')
    media = models.FileField(upload_to='post/')
    type = models.CharField(choices=TYPES, max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def post_media(cls, pk):
        return cls.objects.filter(post=pk)

    def __str__(self):
        return f'media for post {self.post.id}'


class PostMention(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_mentions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_mentions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def user_mentioned_posts(cls, pk):
        return cls.objects.filter(user_id=pk)

    @classmethod
    def post_mentioned_users(cls, pk):
        return cls.objects.filter(post_id=pk)

    def __str__(self):
        return f'mention {self.user.user_name} on post {self.post.id}'

    class Meta:
        unique_together = ('user', 'post')


class StoryMention(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_mentions')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_mentions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def user_mentioned_stories(cls, pk):
        return cls.objects.filter(user_id=pk)

    @classmethod
    def story_mentioned_users(cls, pk):
        return cls.objects.filter(story_id=pk)

    def __str__(self):
        return f'mention {self.user.user_name} on story {self.story.id}'

    class Meta:
        unique_together = ('story', 'user')

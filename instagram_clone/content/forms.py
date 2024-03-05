from django import forms
from .models import Post

from django import forms


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'comment_is_allowed', 'likes_count_display', 'close_friends_only']

    def clean_media_files(self):
        media_files = self.cleaned_data.get('media_files')
        if media_files:
            if len(media_files) > 10:
                raise forms.ValidationError("You can upload up to 10 media files.")
        return media_files

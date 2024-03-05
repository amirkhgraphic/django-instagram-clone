from django import forms
from django.contrib.auth import get_user_model

from user_profile.models import Profile

User = get_user_model()


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'user_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user_name'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['user_name'].widget.attrs['placeholder'] = 'Username'

        self.fields['email'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['bio'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['bio'].widget.attrs['placeholder'] = 'Bio'

        self.fields['image'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['image'].widget.attrs['placeholder'] = 'Image'

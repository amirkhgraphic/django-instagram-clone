from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

User = get_user_model()


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user_name'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['user_name'].widget.attrs['placeholder'] = 'Username'

        self.fields['email'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        self.fields['first_name'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'

        self.fields['password1'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'

        self.fields['password2'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    class Meta:
        model = User
        fields = ('user_name', 'email', 'first_name', 'last_name', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['username'].widget.attrs['placeholder'] = 'Email'

        self.fields['password'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

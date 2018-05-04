# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm, ReadOnlyPasswordHashField

from .models import User


class RegisterForm(UserCreationForm):
    username = forms.RegexField(
        label="Login ID",
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text="Required. 30 characters or fewer. Letters, digits and " "@/./+/-/_ only.",
        error_messages={
            'invalid': "This value may contain only letters, numbers and " "@/./+/-/_ characters."},
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Login ID',
                'required': 'true',
            }))

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': 'true',
            }
        )
    )

    password2 = forms.CharField(
        label="Password confirmation",
        help_text="Enter the same password as above, for verification.",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password confirmation', 'required': 'true',
            }
        )
    )

    email = forms.EmailField(
        label="Firm E-mail",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kim.KIA@hyundai.com',
                'required': 'true',
            }))

    first_name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Name',
                'required': 'true',
            }))

    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Company Phone',
                'required': 'true',
            }))

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "phone")

class ProfileUpdateForm(UserChangeForm):
    username = forms.RegexField(
        label="Employee number(login ID)",
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text="Required. 30 characters or fewer. Letters, digits and " "@/./+/-/_ only.",
        error_messages={
            'invalid': "This value may contain only letters, numbers and " "@/./+/-/_ characters."},
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': 'true',
                'readonly': 'readonly'
            }))

    email = forms.EmailField(
        label="Firm E-mail",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'required': 'true',
            }))

    first_name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': 'true',
            }))

    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': 'true',
            }))

    password = ReadOnlyPasswordHashField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'true',
            }
        )
    )
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "email", "phone")


    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class MyLoginForm(AuthenticationForm):
    username = forms.RegexField(
        label="Username",
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages = { 'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters." },
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': 'true',
            }
        )
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': 'true',
            }
        )
    )

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        help_text="Enter the old password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Old Password',
                'required': 'true',
            }
        )
    )

    new_password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New Password',
                'required': 'true',
            }
        )
    )

    new_password2 = forms.CharField(
        label="Password confirmation",
        help_text="Enter the same password as above, for verification.",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password confirmation', 'required': 'true',
            }
        )
    )
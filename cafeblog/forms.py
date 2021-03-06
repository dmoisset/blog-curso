# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import UserProfile
from django import forms
from cafeblog.models import Blog, Article
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'last_name', 'biography', 'photo')


class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].label = ''
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password'].label = ''
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].label = ''
        self.fields['password2'].widget = forms.PasswordInput()
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-Password'

    class Meta():
        model = User
        fields = (
            'username',
            'email',
            'password'
            )

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords entered do not match")
        return self.cleaned_data


class NewBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description',)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('author', 'blog', 'pub_date', 'creation_time', 'last_modified')

from django import forms
from .models import UserProfileInfo, Produk, Kategori, Comment
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('nama','Tanggal_Lahir','telepon')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserEditProfile(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('Tanggal_Lahir', 'telepon', 'alamat', 'foto_profil')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('nama', 'body')

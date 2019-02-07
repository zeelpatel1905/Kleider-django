from django import forms
from .models import Contact, Profile, Help, Feedback
from django.contrib.auth.models import User

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'content']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'tel', 'gender', 'birth_date', 'img',]

class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ['write']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['write']
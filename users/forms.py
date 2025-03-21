from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm

from .models import User


# Custom UserCreationForm with additional fields 'type' and 'profile_image'
class CustomUserCreationForm(UserCreationForm):
    type = forms.ChoiceField(choices=User.Types.choices, required=True, label="User Type")
    profile_image = forms.ImageField(required=False, label="Profile Image")

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "type", "profile_image", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


# Custom UserChangeForm
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "type", "profile_image")


# Custom SignupForm to align with the user model and handle the 'type' and 'profile_image' fields
class CustomSignupForm(SignupForm):
    type = forms.ChoiceField(choices=User.Types.choices, required=True, label="User Type")

    def save(self, request):
        user = super().save(request)
        user.type = self.cleaned_data['type']  # Save the 'type' field
        user.save()
        return user

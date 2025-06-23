from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile


class UserRegistrationForm(UserCreationForm):
    license_number = forms.CharField(required=False)
    store_name = forms.CharField(required=False)
    contact_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "role", "license_number", "password1", "password2")
        widgets = {
            'role': forms.RadioSelect(choices=User.ROLE_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Exclude admin from choices
        self.fields['role'].choices = [
            choice for choice in User.ROLE_CHOICES if choice[0] != User.ADMIN
        ]

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    store_name = forms.CharField(required=False)
    contact_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
#
# class UserRegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ("username", "email", "phone_number", "role", "license_number", "password1", "password2")
#         widgets = {
#             'password1': forms.PasswordInput(),
#             'role': forms.RadioSelect(choices=User.ROLE_CHOICES),
#         }

    #
    #
    # def __init__(self, *args, **kwargs):
    #     super(UserRegistrationForm, self).__init__(*args, **kwargs)
    #     # Remove 'admin' from role choices
    #     self.fields['role'].choices = [
    #         choice for choice in User.ROLE_CHOICES if choice[0] != User.ADMIN
    #     ]

class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'address_line_1', 'address_line_2', 'address_line_3',
            'district', 'state', 'country', 'zip_code',
            'is_organization', 'organization_name',
            'profile_image', 'cover_image'
        ]
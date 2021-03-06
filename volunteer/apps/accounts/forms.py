from django import forms
from django.contrib.auth import get_user_model

from betterforms.forms import BetterForm, BetterModelForm

from volunteer.apps.profiles.models import Profile

User = get_user_model()


class UserRegistrationForm(BetterForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError(
                'An account with that email address already exists',
            )


class UserRegistrationConfirmForm(BetterModelForm):
    full_name = forms.CharField(required=False, max_length=100)
    display_name = forms.CharField(required=False, max_length=64)
    phone = forms.CharField(required=False, max_length=16)

    has_ticket = forms.BooleanField(label='I have a ticket', required=False)

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = tuple()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserRegistrationConfirmForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_display_name(self):
        display_name = self.cleaned_data['display_name'].strip()
        try:
            p = Profile.objects.get(display_name=display_name)
        except Profile.DoesNotExist:
            return display_name
        else:
            raise forms.ValidationError(
                'The name {0} is already taken by an account using the email address {1}'.format(
                    repr(display_name), repr(p.user.email),
                )
            )


class ProfileForm(BetterModelForm):
    class Meta:
        model = Profile
        fields = ('full_name', 'display_name', 'phone', 'has_ticket')

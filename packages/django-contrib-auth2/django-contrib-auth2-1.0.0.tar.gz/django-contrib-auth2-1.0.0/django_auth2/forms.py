from django import forms

from .conf import get_setting


class LoginForm(forms.Form):
    provider = forms.ChoiceField(
        required=True,
        choices=((key, key) for key, _ in get_setting('AUTH2_PROVIDERS'))
    )
    provider_access_token = forms.CharField(required=True)

    device_id = forms.SlugField(required=True, max_length=128)
    device_name = forms.CharField(required=True, max_length=64)


class LoginRefreshForm(forms.Form):
    refresh_token = forms.SlugField(required=True)
    device_id = forms.SlugField(required=True, max_length=128)

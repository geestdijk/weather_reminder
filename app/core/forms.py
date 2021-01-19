from django import forms


class SignUpForm(forms.Form):

    email = forms.CharField(max_length=255)
    name = forms.CharField(max_length=255)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)

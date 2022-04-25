from django import forms

class RegisterationForm(forms.Form):
    email = forms.EmailField(label='Your Email')



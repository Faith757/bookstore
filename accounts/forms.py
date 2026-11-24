from django import forms

class Login(forms.Form):
    email = forms.EmailField(
        label = 'Email Address',
        widget = forms.EmailInput(attrs={
            'placeholder': 'Enter email address',
            'class': 'loginform'
        })
    )

class verification(forms.Form):
    otp = forms.CharField(
        min_length = 6, 
        max_length = 6,
        label = "Enter OTP",
        widget = forms.TextInput(attrs={
            'class': 'loginform',
            'inputmode': 'numeric'
        })
    )
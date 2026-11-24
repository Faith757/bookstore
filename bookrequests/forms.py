from django import forms
from .models import bookRequest

class requestForm(forms.ModelForm):
    class Meta:
        model = bookRequest
        fields = ['title', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter book title'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Category'
            }),
        }
from django import forms
from main.models import Contact_requirement
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.ModelForm):
    name = forms.CharField(min_length=4,
        widget = forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': 'Họ và tên',
            'required':True
        }), error_messages = {'required':'Bắt buộc'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'}))

    phone_number = forms.CharField(min_length=9, widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Số điện thoại'
    }))

    message = forms.CharField(widget = forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Chúng tôi có thể giúp gì bạn?',
        'required':True

    }))

    #responded = forms.BooleanField(widget=forms.HiddenInput(), initial=False)


    class Meta:
        model = Contact_requirement
        exclude = ['responded']

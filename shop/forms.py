from django import forms
from django.forms import ModelForm, ValidationError

from shop.models import Order, Reviews


class OrderModelForm(ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'phone_number', 'email', 'address', 'notice']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg mb-3'}
            ),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control form-control-lg mb-3'}
            ),
            'email': forms.TextInput(
                attrs={'class': 'form-control form-control-lg mb-3'}
            ),
            'address': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg mb-3',
                    'rows': 4
                }
            ),
            'notice': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg mb-3',
                    'rows': 4
                }
            ),
        }

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if data.isalpha():
            raise ValidationError('Введите номер телефона')
        return data


class ReviewsAddForm(ModelForm):

    class Meta:
        model = Reviews
        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg mb-3'}
            ),
            'email': forms.TextInput(
                attrs={'class': 'form-control form-control-lg mb-3'}
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg mb-3',
                    'rows': 6
                }
            ),
        }

    def clean_name(self):
        data = self.cleaned_data['name']
        if data == '':
            raise ValidationError('Введите пожалуйста имя')
        return data

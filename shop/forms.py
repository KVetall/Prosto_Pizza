from django.forms import ModelForm, RegexField, Textarea, ValidationError

from shop.models import Order


class OrderModelForm(ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'phone_number', 'email', 'address', 'notice']
        widgets = {
            'address': Textarea(
            attrs={'rows': 6, 'placeholder': 'Пожалуйста, укажите адрес доставки'}
            ),
            'notice': Textarea(
            attrs={'rows': 6}
            ),
        }

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if data.isalpha():
            raise ValidationError('Введите номер телефона')
        return data

from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('service_name', 'host_name', 'port')
        widgets = {
            'service_name': forms.TextInput(attrs={'placeholder': 'Please input service name.'}),
            'host_name': forms.TextInput(attrs={'placeholder': 'Please input host name.'}),
            'port': forms.NumberInput(attrs={'placeholder': 'Please input port number.', 'min': 1}),
        }

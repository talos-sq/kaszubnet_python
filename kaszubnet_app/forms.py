from django import forms
from kaszubnet_app.models import *

ITEM_TYPE = [
    (0, 'Nieznany'),
    (1, 'Użytkowy'),
    (2, 'Materiał do produkcji'),
    (3, 'Medyczny'),
    (4, 'Elektronika'),
]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Wprowadź login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Wprowadź hasło'}))


class WarehouseActionForm(forms.ModelForm):
    item_name = forms.CharField(max_length=64,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'item_name_input'}))
    item_type = forms.ChoiceField(choices=ITEM_TYPE,
                                  widget=forms.Select(attrs={'class': 'form-select', 'id': 'item_type_input'}))
    item_amount = forms.DecimalField(initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'item_amount_input'}))
    item_description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'item_des_input', 'rows': '4'}))

    class Meta:
        model = WarehouseItems
        fields = ['item_name', 'item_type', 'item_amount', 'item_description']

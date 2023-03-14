from django import forms
from kaszubnet_app.models import *

ITEM_TYPE = [
    (0, 'Nieznany'),
    (1, 'Użytkowy'),
    (2, 'Materiał do produkcji'),
    (3, 'Medyczny'),
    (4, 'Elektronika'),
]
ACTION_TYPE = [
    (0, 'Przyjęcie'),
    (1, 'Wydanie'),
]


class LabelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.item_name}"


class LabelChoiceField2(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name}"


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Wprowadź login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Wprowadź hasło'}))


class WarehouseActionAddForm(forms.ModelForm):
    item_name = forms.CharField(max_length=64,widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'item_name_input'}))
    item_type = forms.ChoiceField(choices=ITEM_TYPE,widget=forms.Select(
        attrs={'class': 'form-select', 'id': 'item_type_input'}))
    item_amount = forms.DecimalField(initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'item_amount_input'}))
    item_description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'item_des_input', 'rows': '4'}))

    class Meta:
        model = WarehouseItems
        fields = ['item_name', 'item_type', 'item_amount', 'item_description']


class WarehouseActionUpdateForm(forms.Form):
    action_type = forms.ChoiceField(choices=ACTION_TYPE, widget=forms.Select(
        attrs={'class': 'form-select', 'id': 'type_input'}))
    client = LabelChoiceField2(queryset=Character.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select', 'id': 'client_input'}))
    item = LabelChoiceField(queryset=WarehouseItems.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select', 'id': 'item_input'}))
    amount = forms.DecimalField(initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'amount_input'}))
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'item_des_input', 'rows': '4'}))

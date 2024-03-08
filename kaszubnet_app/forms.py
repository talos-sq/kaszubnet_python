from django import forms
from kaszubnet_app.models import *
from django.contrib.auth import get_user_model

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


class NewCharacterForm(forms.ModelForm):
    user = get_user_model()

    name = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'id': 'name'}))
    owner = LabelChoiceField(queryset=user.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select', 'id': 'owner'}))
    birthdate = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'birthdate'}), required=False)
    rank = forms.ChoiceField(choices=RANKS, widget=forms.Select(
        attrs={'class': 'form-select', 'id': 'rank'}))
    function = forms.ChoiceField(choices=FUNCTION, widget=forms.Select(
        attrs={'class': 'form-select', 'id': 'function'}))
    # abilities = forms.ManyToManyField(Ability, blank=True, verbose_name="Umiejętności")
    outpost = forms.ChoiceField(choices=OUTPOSTS, widget=forms.Select(
        attrs={'class': 'form-select', 'id': 'outpost'}))
    origin_outpost = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'origin_outpost'}), required=False)
    job = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'job'}), required=False)
    specialization = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'specialization'}), required=False)
    religion = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'religion'}), required=False)
    character_history = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'character_history', 'rows': '4'}), required=False)
    # old_town_presence = models.ManyToManyField(OTs, null=True, blank=True, verbose_name="Pory Przybyszów")
    # dead = forms.BooleanField(null=True, blank=True, verbose_name="Czy postać zmarła?")
    # left_faction = models.BooleanField(null=True, blank=True, verbose_name="Czy postać opuściła frakcje?")
    picture = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'picture'}), required=False)

    owner = get_user_model()

    class Meta:
        model = Character
        fields = ['name', 'owner', 'birthdate', 'rank', 'function', 'outpost', 'origin_outpost', 'job',
                  'specialization',
                  'religion', 'character_history']


class WarehouseActionAddForm(forms.ModelForm):
    item_name = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'item_name_input'}))
    item_type = forms.ChoiceField(choices=ITEM_TYPE, widget=forms.Select(
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


class CharacterAvatarForm(forms.Form):
    picture = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'picture'}))


class CharacterForm(forms.ModelForm):
    pass

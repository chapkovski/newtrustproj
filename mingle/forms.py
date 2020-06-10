import django.forms as forms
from .models import MegaSession, MingleSession
from django.forms import inlineformset_factory




class MegaForm(forms.ModelForm):
    """Form for individual checkbox"""
    mingles = forms.ModelMultipleChoiceField(
        queryset=MingleSession.objects.filter(megasession__isnull=True),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = MegaSession
        fields = ['id']

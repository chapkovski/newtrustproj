import django.forms as forms
from .models import MegaSession, MingleSession
from django.forms import inlineformset_factory
from django.db.models import Q


class MegaForm(forms.ModelForm):
    """Form for individual checkbox"""

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        initial_query = MingleSession.objects.filter(Q(megasession=instance) ) if instance else None
        self.fields['mingles'] = forms.ModelMultipleChoiceField(
            queryset=MingleSession.objects.filter(Q(megasession=instance) | Q(megasession__isnull=True)),
            widget=forms.CheckboxSelectMultiple,
            initial= initial_query)

    class Meta:
        model = MegaSession
        fields = ['id']

import django.forms as forms
from .models import MegaSession, MingleSession
from django.forms import inlineformset_factory, modelformset_factory
from django.db.models import Q


class CustomMingleForm(forms.ModelForm):
    class Meta:
        model = MingleSession
        fields = ['megasession']

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.fields['megasession'] = forms.BooleanField(
            widget=forms.CheckboxInput,
            required=False
        )

    def clean_megasession(self):
        val = self.cleaned_data['megasession']
        print('VAL????', val, self.owner)
        if val:
            return self.owner
        else:
            return None


MingleFormSet = modelformset_factory(model=MingleSession, form=CustomMingleForm, extra=0, can_delete=False)


class MegaForm(forms.ModelForm):
    """Form for individual checkbox"""

    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get('instance')
    #     super().__init__(*args, **kwargs)
    #     initial_query = MingleSession.objects.filter(Q(megasession=instance)) if instance else None
    #     self.fields['mingles'] = forms.ModelMultipleChoiceField(
    #         queryset=MingleSession.objects.filter(Q(megasession=instance) | Q(megasession__isnull=True)),
    #         widget=forms.CheckboxSelectMultiple,
    #         initial=initial_query)

    class Meta:
        model = MegaSession
        fields = ['id']

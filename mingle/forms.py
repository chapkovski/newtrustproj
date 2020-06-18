import django.forms as forms
from .models import MegaSession, MingleSession
from django.forms import inlineformset_factory, modelformset_factory, BaseModelFormSet
from django.db.models import Q


class MingleFormSet(BaseModelFormSet):
    def clean(self):
        nones = [form.cleaned_data.get('megasession') is None for form in self.forms]

        if all(nones):
            raise forms.ValidationError('You should choose at least one session')
        pass


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
        if val:
            return self.owner
        else:
            return None


MingleFormSet = modelformset_factory(
    model=MingleSession,
    form=CustomMingleForm,
    formset=MingleFormSet,
    extra=0,
    can_delete=False
)


class MegaForm(forms.ModelForm):
    """Form for individual checkbox"""

    class Meta:
        model = MegaSession
        fields = ['id']

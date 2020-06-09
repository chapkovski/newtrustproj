import django.forms as forms
from .models import MegaSession, MingleSession
from django.forms import inlineformset_factory


class MingleFormset(forms.BaseInlineFormSet):
    model = MingleSession

    def get_queryset(self):
        print('HWAT??', self.model.objects.filter(wrapper__isnull=True))
        return self.model.objects.filter(wrapper__isnull=True)


class MegaForm(forms.ModelForm):
    """Form for individual checkbox"""
    mingles = forms.ModelMultipleChoiceField(
        queryset=MingleSession.objects.filter(wrapper__isnull=True),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = MegaSession
        fields = ['comment']

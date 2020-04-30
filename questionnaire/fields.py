from otree.models import StringField
from django.db.models import CharField
from django.forms.fields import MultiValueField, CharField, MultipleChoiceField, ChoiceField
class MultiBlocker(StringField):
    def formfield(self, **kwargs):
        if self.inner_choices is not None:
            return MultiSelectFormField(choices=self.inner_choices,
                                        label=self.verbose_name, required=not self.blank,
                                        widget=NoCheckboxCheckbox(choices=self.inner_choices),
                                        max_choices=self.max_choices,
                                        min_choices=self.min_choices,
                                        **kwargs)

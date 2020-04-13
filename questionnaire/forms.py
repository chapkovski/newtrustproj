import django.forms as forms
from otree.forms import ModelForm
from collections import OrderedDict


class TrustForm(ModelForm):
    def __init__(self, joined_fields, *args, view=None, **kwargs):
        self.joined_fields = joined_fields
        self.view = view
        super().__init__(*args, **kwargs)
        firstfield = joined_fields[0]
        first_chosen_field = [v for f, v in self.fields.items() if f in firstfield['fields']][0]
        self.joined_fields[0]['choices'] = first_chosen_field.widget.choices

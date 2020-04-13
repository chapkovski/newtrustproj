import django.forms as forms
from otree.forms import ModelForm
from collections import OrderedDict
from otree.api import widgets


class TrustForm(ModelForm):
    def __init__(self, joined_fields, *args, view=None, **kwargs):
        flattened_joined_fields = [i for j in joined_fields for i in j['fields']]
        self.joined_fields = joined_fields
        self.view = view
        super().__init__(*args, **kwargs)
        for jfield in joined_fields:
            fields = jfield['fields']
            for f, v in self.fields.items():
                if f in fields:
                    stripped_choices = [ch for ch in v.widget.choices if ch[0] != '']
                    self.fields[f].widget = widgets.RadioSelectHorizontal(choices=stripped_choices)

            first_chosen_field = [v for f, v in self.fields.items() if f in jfield['fields']][0]
            jfield['choices'] = first_chosen_field.widget.choices
        self.non_joined_fields = [f for f in self.fields.keys() if f not in flattened_joined_fields]

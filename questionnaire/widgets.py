from otree.forms.widgets import RadioSelect


class OtherRadioSelect(RadioSelect):
    template_name = 'questionnaire/widgets/radio.html'

    def __init__(self, other=None, *args, **kwargs):
        self.other = other
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        c = super().get_context(name, value, attrs)
        c['other'] = self.other
        return c

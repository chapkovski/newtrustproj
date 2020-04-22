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


from django import forms


class LikertWidget(forms.RadioSelect):
    template_name = 'questionnaire/widgets/likert.html'

    class Media:
        css = {
            'all': ('likert.css',)
        }

    def __init__(self, quote, label, left, right,  *args, **kwargs):
        self.quote = quote
        self.label = label
        self.left = left
        self.right = right

        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)


        context.update({'choices': self.choices,
                        'quote': self.quote,
                        'label': self.label,
                        'left': self.left,
                        'right': self.right,
                        'optimal_width': round(85 / len(self.choices), 2),

                        })
        return context

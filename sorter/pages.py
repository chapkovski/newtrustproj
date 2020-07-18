from questionnaire.generic_pages import Page
from django.conf import settings

class Intro(Page):
    pass
class Intro2(Page):
    pass
class ExchangeRate(Page):
    pass


class Code(Page):
    form_model = 'player'
    form_fields = ['city']

    def vars_for_template(self):
        return dict(GOOGLE_API_KEY=settings.GOOGLE_API_KEY)


page_sequence = [
    Intro,
    Intro2,
    ExchangeRate,
    Code
]

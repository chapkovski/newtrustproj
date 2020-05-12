from questionnaire.generic_pages import Page



class Code(Page):
    form_model = 'player'
    form_fields = ['city']






page_sequence = [Code]

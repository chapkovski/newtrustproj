from ._builtin import Page, WaitPage
from typing import List
import otree.bots.browser as browser_bots
from .cq_models import correct_answers


class SenderPage(Page):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset(instance=self.player)
        return context

    def is_displayed(self) -> bool:
        return self.player.role() == 'Sender'


class ReturnerPage(Page):
    def is_displayed(self) -> bool:
        return self.player.role() != 'Sender'


class FormSetMixin:
    formset = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset(instance=self.player)
        return context

    def get_form(self, data=None, files=None, **kwargs):
        return self.formset(data, instance=self.player)


class CQPage(Page):
    form_model = 'player'
    page = None

    def is_displayed(self) -> bool:
        return self.session.config.get('cq', False)

    def get_form_fields(self) -> List[str]:
        return [k for k in correct_answers.keys() if k.startswith(f'cq{self.page}')]

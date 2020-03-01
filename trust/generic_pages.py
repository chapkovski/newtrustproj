from ._builtin import Page, WaitPage
import otree.bots.browser as browser_bots


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

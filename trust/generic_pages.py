from ._builtin import WaitPage
from questionnaire.generic_pages import Page
from typing import List
from django.db.models import Avg
from .cq_models import correct_answers


class SenderPage(Page):

    def is_displayed(self) -> bool:
        return self.player.role() == 'sender'


class ReturnerPage(Page):
    def is_displayed(self) -> bool:
        return self.player.role() != 'sender'


class FormSetMixin:
    formset = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset(instance=self.player, decision_type=self.decision_type)
        return context

    def get_form(self, data=None, files=None, **kwargs):
        # here if this page was forced by admin to continue we just submit an empty form (with no formset data)
        # if we need this data later on that can create some problems. But that's the price we pay for autosubmission
        if data and data.get('timeout_happened'):
            return super().get_form(data, files, **kwargs)
        return self.formset(data=data, instance=self.player, decision_type=self.decision_type)


from .forms import cq_formset


class CQPage(Page):
    part = None
    role = None
    custom_general_error = True

    def is_displayed(self) -> bool:
        return self.session.config.get('cq', False)

    def get_cq_instances(self):
        """Get cq for this part and this role"""
        return [q for q in self.player.cqs.all() if q.role == self.role and q.part == self.part]

    def get_formset(self, data=None):
        """Get formset with cq instnaces"""
        return cq_formset(instance=self.player, data=data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def get_form(self, data=None, files=None, **kwargs):
        # here if this page was forced by admin to continue we just submit an empty form (with no formset data)
        # if we need this data later on that can create some problems. But that's the price we pay for autosubmission
        if data and data.get('timeout_happened'):
            return super().get_form(data, files, **kwargs)
        return self.get_formset(data=data)

    def before_next_page(self):
        counter_name = f'cq{1}_counter'
        counter = self.player.cqs.filter(part=self.part, role=self.role).aggregate(avg=Avg('counter'))['avg']
        setattr(self.player, counter_name, counter)

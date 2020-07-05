from ._builtin import WaitPage
from questionnaire.generic_pages import Page
from typing import List
from django.db.models import Avg



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
    custom_general_error = True

    def is_displayed(self) -> bool:
        return self.session.config.get('cq', False)

    def get_cq_instances(self):
        """Get cq for this part and this role"""
        cqs_for_this_part = self.player.cqs.filter(part=self.part, role=None)
        cqs_for_this_role = self.player.cqs.filter(part=self.part, role=self.player.role())
        return (cqs_for_this_part | cqs_for_this_role)

    def get_formset(self, data=None):
        """Get formset with cq instnaces"""
        return cq_formset(instance=self.player, data=data, queryset=self.get_cq_instances())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        # let's set counter:
        q = self.get_cq_instances()
        q.filter(counter__isnull=True).update(counter=0)
        return context


    def get_form(self, data=None, files=None, **kwargs):
        # here if this page was forced by admin to continue we just submit an empty form (with no formset data)
        # if we need this data later on that can create some problems. But that's the price we pay for autosubmission
        if data and data.get('timeout_happened'):
            return super().get_form(data, files, **kwargs)
        if not data:
            return self.get_formset()
        formset = self.get_formset(data=data)
        return formset


    def before_next_page(self):
        counter_name = f'cq{self.part}_counter'
        counter = self.get_cq_instances().aggregate(avg=Avg('counter'))['avg']
        setattr(self.player, counter_name, counter)

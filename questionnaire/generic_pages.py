from ._builtin import Page as oTreePage

from .forms import UpdatedOtreeForm
from django.forms.models import modelform_factory
from django.conf import settings
from django.utils import translation


class TransMixin:
    def get_context_data(self, **context):
        user_language = self.session.config.get('language', settings.LANGUAGE_CODE)
        translation.activate(user_language)
        return super().get_context_data(**context)


class Page(TransMixin, oTreePage):
    joined_fields = None

    def get_progress(self):
        totpages = self.participant._max_page_index
        curpage = self.participant._index_in_pages
        return f"{curpage / totpages * 100:.0f}"

    def get_form_class(self):
        form_model = self._get_form_model()
        fields = self.get_form_fields()
        return modelform_factory(form_model, fields=fields, form=UpdatedOtreeForm)

    def get_form(self, data=None, files=None, **kwargs):
        cls = self.get_form_class()
        return cls(self.joined_fields, data=data, files=files, view=self, **kwargs)


from ._builtin import Page as oTreePage


from .forms import UpdatedOtreeForm
from django.forms.models import modelform_factory


class Page(oTreePage):
    joined_fields = None

    def get_form_class(self):
        form_model = self._get_form_model()
        fields = self.get_form_fields()
        return modelform_factory(form_model, fields=fields, form=UpdatedOtreeForm)

    def get_form(self, data=None, files=None, **kwargs):
        cls = self.get_form_class()
        return cls(self.joined_fields, data=data, files=files, view=self, **kwargs)

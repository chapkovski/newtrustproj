from ._builtin import Page as oTreePage

from .forms import UpdatedOtreeForm
from django.forms.models import modelform_factory
from django.conf import settings
from django.utils import translation
from trust.models import TimeTracker
from datetime import datetime,timezone
import time, random

class TransMixin:

    def get_context_data(self, **context):
        user_language = self.session.config.get('language', settings.LANGUAGE_CODE)
        translation.activate(user_language)
        return super().get_context_data(**context)


class Page(TransMixin, oTreePage):
    joined_fields = None

    def get(self, *args, **kwargs):
        t, _ = TimeTracker.objects.get_or_create(owner=self.participant,
                                                 page=self.__class__.__name__,
                                                 period=self.player.round_number,
                                                 defaults=dict(get_time=datetime.now(timezone.utc), ))
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.participant.is_browser_bot:
            time.sleep(random.randint(0,5))
        try:
            t = TimeTracker.objects.get(owner=self.participant,
                                        page=self.__class__.__name__,
                                        period=self.player.round_number,
                                        )
            t.post_time = datetime.now(timezone.utc)
            t.seconds_on_page = (t.post_time-t.get_time).seconds
            t.save()
        except TimeTracker.DoesNotExist:
            pass

        return super().post(*args, **kwargs)

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

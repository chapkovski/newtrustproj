from ._builtin import Page, WaitPage


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

    def post(self):
        import otree.bots.browser as browser_bots
        if self.participant.is_browser_bot:
            print("BEFORE SUBMISSIONS!!!!!")
            submission = browser_bots.get_next_post_data(
                participant_code=self.participant.code
            )
            print('SUBMISSION', submission)
            raise Exception('JJJJ')
        self.object = self.get_object()
        self.form = self.get_form(
            data=self.request.POST, files=self.request.FILES, instance=self.object)

        formset = self.formset(self.request.POST, instance=self.player)

        if not formset.is_valid():
            context = self.get_context_data()
            context['formset'] = formset
            self.form.add_error(None, 'all fields are required!')
            context['form'] = self.form
            return self.render_to_response(context)
        formset.save()
        return super().post()

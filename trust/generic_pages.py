from ._builtin import Page, WaitPage


class SenderPage(Page):
    def is_displayed(self) -> bool:
        return self.player.role() == 'Sender'


class ReturnerPage(Page):
    def is_displayed(self) -> bool:
        return self.player.role() != 'Sender'

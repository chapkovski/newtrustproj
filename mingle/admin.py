from django.contrib import admin
from django.apps import apps
from otree.models import Participant, Session
from .models import MegaSession, MingleSession, MegaParticipant
from django.utils.html import format_html
from django.shortcuts import resolve_url
from django.contrib.admin.templatetags.admin_urls import admin_urlname

"""Our goal here:
1. To show group members and their decisions as a tabular in MegaGroup and Pseudogroup
2. For each session (via proxy) show participants, the group they belong to, and their partner
3. at lists show most of params. especially for megaparticipant.
  
"""


@admin.register(MegaParticipant)
class MGPAdmin(admin.ModelAdmin):
    readonly_fields = ['owner_code', 'partner_code', 'city', 'role', 'guess', 'decision', 'other_decision',
                       'payoff1',
                       'payoff2',
                       'payoff',
                       ]
    list_display = ['owner_code', 'city_short',
                    'role', 'megasession', 'group', 'pseudogroup']

    def owner_code(self, instance):
        return instance.owner.code

    def partner_code(self, item):
        url = resolve_url(admin_urlname(MegaParticipant._meta, 'change'), item.group_partner().id)
        return format_html('<a href="{url}">{name}</a>'.format(url=url, name=str(item.group_partner().owner.code)))

    def role(self, instance):
        return instance.player._role

    def city(self, instance):
        return instance.player.city.description

    def guess(self, instance):
        return instance.guess

    def decision(self, instance):
        return instance.decision

    def other_decision(self, instance):
        return instance.group_partner().decision

    def payoff1(self, instance):
        return instance.player.stage1payoff

    def payoff2(self, instance):
        return instance.player.stage2payoff

    def payoff(self, instance):
        return instance.player.payoff

    def city_short(self, instance):
        city = self.city(instance)
        i = city.find('(')
        return city[:i]


class MSSessionInline(admin.TabularInline):
    show_change_link = True
    extra = 0
    can_delete = False
    exclude = ['owner']
    readonly_fields = ('owner_code',)
    model = MingleSession

    def owner_code(self, instance):
        return instance.owner.code

    def has_add_permission(self, request, obj):
        return False


@admin.register(MegaSession)
class MSAdmin(admin.ModelAdmin):
    fields = ['comment', 'payoff_calculated', 'groups_formed']

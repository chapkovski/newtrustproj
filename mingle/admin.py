from django.contrib import admin
from trust.models import CQ
from .models import (MegaSession, MingleSession, MegaParticipant,
                     MegaGroup, PseudoGroup)
from django.utils.html import format_html
from django.shortcuts import resolve_url
from django.contrib.admin.templatetags.admin_urls import admin_urlname

"""Our goal here:
1. To show group members and their decisions as a tabular in MegaGroup and Pseudogroup
2. For each session (via proxy) show participants, the group they belong to, and their partner
3. at lists show most of params. especially for megaparticipant.
  
"""


@admin.register(CQ)
class CQdmin(admin.ModelAdmin):
    list_display = ['owner_code', 'session', 'text', 'choices','counter',]
    list_display_links = list_display

    def owner_code(self, instance):
        return instance.owner.participant.code

    def session(self, instance):
        return instance.owner.session.code

@admin.register(MegaParticipant)
class MGPAdmin(admin.ModelAdmin):
    list_display = ['owner_code', 'city_short',
                    'role', 'megasession', 'group', 'pseudogroup']

    def owner_code(self, instance):
        return instance.owner.code

    def city_short(self, instance):
        return instance.city.eng


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


@admin.register(MingleSession)
class MingleAdmin(admin.ModelAdmin):
    list_display = ['owner_code', 'megasession', 'created_at', 'updated_at']
    list_display_links = ['owner_code', 'megasession', 'created_at', 'updated_at']

    def owner_code(self, instance):
        return instance.owner.code


class GGAdmin(admin.ModelAdmin):
    list_display = ['link', ]
    list_display_links = ['link']

    def link(self, instance):
        return f'Group id {instance.id}'

    def role_player(self, instance, role):
        p = instance.get_player_by_role(role).participant
        m = p.megaparticipant
        url = resolve_url(admin_urlname(MegaParticipant._meta, 'change'), m.id)
        name = p.code
        if m.group is None:
            name += ' (ungrouped)'
        return format_html('<a href="{url}">{name}</a>'.format(url=url, name=name))

    def sender(self, instance):
        return self.role_player(instance, 'sender')

    def receiver(self, instance):
        return self.role_player(instance, 'receiver')


@admin.register(MegaGroup)
class MGAdmin(GGAdmin):
    pass


@admin.register(PseudoGroup)
class PGAdmin(GGAdmin):
    pass

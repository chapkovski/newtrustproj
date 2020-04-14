from django import template

from django.utils.safestring import mark_safe

register = template.Library()
import re


@register.filter
def rubl(value):
    value = str(value)
    p = re.compile(r'^(?P<value>\d+)')
    m = p.search(value)
    re_val = m.group('value')
    if re_val:
        intval = int(re_val)
        lastdigit = int(re_val[-1])
        if 5 <= intval <= 20:
            r = 'рублей'
        elif 2 <= lastdigit <= 4:
            r = 'рубля'
        elif lastdigit == 1:
            r = 'рубль'
        else:
            r = 'рублей'

        return re_val + " " + r
    return value


@register.inclusion_tag('questionnaire/tags/joined_form.html', name='joined_form')
def render_joined_form(form):
    return {'form': form}

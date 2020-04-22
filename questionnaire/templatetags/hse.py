from django import template
from otree.templatetags.otree_forms import FormFieldNode
from django.utils.safestring import mark_safe

register = template.Library()
import re


class HSEFormField(FormFieldNode):
    default_template = 'questionnaire/tags/hsefield.html'

register.tag('hsefield', HSEFormField.parse)

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


@register.inclusion_tag('questionnaire/tags/joined_form.html', name='joined_form', takes_context=True)
def render_joined_form(context, form):


    return dict(form=form,
                fields_order=getattr(context['view'], 'jfields_order', [])
                )

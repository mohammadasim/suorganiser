from django.core.exceptions import \
    ImproperlyConfigured
from django.urls import reverse
from django.template import (
    Library, TemplateSyntaxError
)
from django.utils.safestring import mark_safe

register = Library()


@register.inclusion_tag('core/includes/form.html',
                        takes_context=True)
def form(context, *args, **kwargs):
    """
    function to define form custom tag.
    We expect three args or kwargs. If
    action is not set we raise an error
    and then simply return these values
    as context to the template being
    included.
    The form is taken from the context
    of the template calling this template
    tag.
    The function also receives bootstrap
    button CSS classes that will be added
    to the button.
    """
    button_classes = kwargs.get('button_classes')
    action = (args[0] if len(args) > 0
              else kwargs.get('action'))
    button = (args[1] if len(args) > 1
              else kwargs.get('button'))
    method = (args[2] if len(args) > 2
              else kwargs.get('method'))
    form = context.get('form')
    if action is None:
        raise TemplateSyntaxError(
            'form template tag requires'
            'at least one argument: action,'
            'which is a URL.')
    if button_classes is None:
        button_css = ''
    else:
        button_css = mark_safe(button_classes)
    return {
        'form': form,
        'button': button,
        'action': action,
        'method': method,
        'button_css': button_css
    }


@register.inclusion_tag(
    'core/includes/confirm_delete_form.html',
    takes_context=True
)
def delete_form(context, *args, **kwargs):
    pass

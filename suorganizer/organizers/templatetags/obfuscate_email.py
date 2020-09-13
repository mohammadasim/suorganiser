"""
Django looks for any custom template tags
in the templatetags directory and treats them
as a namespace. A custom tag in one app is
available for all apps. The name of the file
is the name we use to load the custom template
filter in the template.
We import the entirety of Django's template
package, then import the @stringfilter
decorator. This decorator is a shortcut that
allows us to build our filter quickly. It
tells Django that our function accepts a string
as our only argument.
When it loads our file in the template, Django
expects to find a valid template library, with
tags and filters registered to that library.
Hence we create a library instance, which we
then use to register our custom tags and filters.
"""
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter('obfuscate', is_safe=False)
@stringfilter
def obfuscate_email(value):
    """
    The first decorator registers the
    filter as obfuscate with the library instance.
    The is_safe set to false, tells Django
    that the string that this function returns
    is not safe, we have not escaped by HTML
    special characters or ensured there is no
    malicious code in the string being returned.
    The second decorator tells Django
    that our filter accepts string.
    Given an email address in a string
    this function will remove the '@'
    and replace it with 'at' and replace
    '.' with 'dot'.
    """
    return (
        value
        .replace('@', ' at ')
        .replace('.', ' dot ')
    )

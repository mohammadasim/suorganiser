"""
When building more complex template tags
Django cannot provide a decorator to
make it easy. Instead we must deal with
the objects that Django uses internally
For a template tag Django expects the
creation of a function and a subclass
of the Node class.
Here we create a custom template tag
that adds a list of the most recent
blog posts to our template context.
"""

from django.template import (
    Library, Node, TemplateSyntaxError
)
from ..models import Post

register = Library()


@register.tag(name='get_latest_post')
def do_latest_post(parser, token):
    """
    By convention most template tag
    functions start with do.
    Function returns a LatestPostNode
    object. The render method of this
    object adds a single latest post
    object to the context, that is
    then returned to the template.
    """
    return LatestPostNode()


@register.tag(name='get_latest_posts')
def do_latest_posts(parser, token):
    """
    function that returns an instance
    of LatestPostsNode. The render
    method of the instance adds a
    list of latest post object.
    The number of posts objects in
    the list is equal to the number
    passed to the tag as an argument.
    To get the number, the whole tag call
    is passed as a string in an object.
    This string is accessible as the
    content attribute of token object.
    """
    try:
        """
        Using splint_contents() is the most
        robust option available. It should be
        used instead of token.content.split()
        because split_content() respects variables
        grouped by quotation marks. The call to 
        immaginary template tag {% fiction 'hello world %}
        will be split by slit_content as ('fiction', 'hello world')
        whereas by token.content.split as ('fiction', 'hello', 'world')
        """
        tag_name, number_of_posts_str = (
            token.split_content()
        )
    except ValueError:
        raise TemplateSyntaxError(
            'get_latest_posts_take 1 argument: '
            'number of posts to get'
                    )
    try:
        number_of_posts = int(number_of_posts_str)
    except ValueError:
        raise TemplateSyntaxError(
            "tag '{tag_display}' sole argument "
            "must be an integer".format(
                tag_display=tag_name
            )
        )
    return LatestPostsNode(number_of_posts)




class LatestPostNode(Node):
    """
    A sub class of Node returning
    a single latest post.
    The Node class defines the
    render() which accepts a template
    context and then prints a value.
    In this case we are not interested
    in displaying anything, we instead
    want to add a value to the context
    """

    def render(self, context):
        """
        Overriding the method to
        add latest posts to the
        context
        """
        context['latest_post'] = \
            Post.objects.published().latest()
        return str()


class LatestPostsNode(Node):
    """
    Node subclass returning
    a list of latest posts.
    """


def __init__(self, number_of_posts):
    self.num = number_of_posts


def render(self, context):
    """
    Overriding the method
    in the Node class
    """
    context['latest_post_list'] = \
        Post.objects.published[:self.num]
    return str()

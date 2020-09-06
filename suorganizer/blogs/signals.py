"""
Signal model for blogs
"""
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from organizers.models import Tag

from .models import Post


@receiver(m2m_changed,
          sender=Post.startups.through)
def assign_extra_tags(sender, **kwargs):
    """
    Function to assign extra tags to the
    posts. These tags are associated with
    startup, which is associated with the
    post object.
    In django the table representing m2m
    relationship is called through. We are
    referencing the table using the relationship
    from Post, but the same table can also be
    accessed from startup as, Startup.blog_posts.through
    :param sender:
    :param kwargs:
    :return:
    """
    action = kwargs.get('action')
    if action == 'post_add':
        reverse = kwargs.get('reverse')
        if not reverse:
            # In the event of a forward relation, the post
            # instance is assigned to the instance keyword.
            # While the list of startup primary keys being
            # associated to the post object is passed to
            # pk_set keyword.The Startup is assigned to
            # the model keyword. I have commented it out
            # because we are not going to use the startup.
            post = kwargs.get('instance')
            # Startup = kwargs.get('model')
            startup_pk_set = kwargs.get('pk_set')
            # The in lookup available to managers and
            # querysets finds all the values in a list.
            # In our case we are using the in lookup on
            # our tags to find out all the tags associated
            # with the startups, that have pk in startup_pk_set keyword.
            # We then call the values_list method on the queryset
            # to give us a flat list of primary keys.
            # We then use the distinct() to make sure the pk are unique.
            # iterator() method is used to ensure, django doesn't cache
            # our queryset.
            tag_pk_set = Tag.objects.filter(startup__in=startup_pk_set) \
                .values_list('pk', flat=True).distinct() \
                .iterator()
            post.tags.add(*tag_pk_set)
        else:
            startup = kwargs.get('instance')
            post = kwargs.get('model')
            post_pk_set = kwargs.get('pk_set')
            # We use the relatedManager, that is created
            # for m2m and foreign key relation to call
            # the values_list() method to retrieve the
            # pk of the tags associated with a startup
            tags_associated_with_startup = startup.tags.values_list(
                'pk', flat=True
            ).iterator()
            # We then use the in_bulk queryset method to load
            # the post objects in post_pk_set
            post_dict = post.objects.in_bulk(post_pk_set)
            # We then get the values of the dict that is
            # a list of post objects and iterate over them
            # The tags associated with startup are then
            # added to the post.
            for post in post_dict.values:
                post.tags.add(tags_associated_with_startup)

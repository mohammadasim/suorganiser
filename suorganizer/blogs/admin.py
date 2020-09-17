from datetime import datetime

from django.contrib import admin
from django.db.models import Count

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Creating a sub class of model admin
    to modify the behaviour of Post model
    in the admin app.
    """

    # Aggregate functions allow us to perform
    # calculations directly in the database
    # As calling the database is an expensive
    # operation
    def get_queryset(self, request):
        """
        overriding the default method
        to perform tag count at
        database level
        Also allowing only users with
        permissions to see future
        publishing posts.
        :param request:
        :return:
        """
        queryset = super().get_queryset(request)
        if not request.user.has_perms(
                'view_future_post'
        ):
            queryset = queryset.filter(
                pub_date__lte=datetime.now()
            )
        # This is optimisation to reduce
        # calls to the database.
        return queryset.annotate(
            tag_number=Count('tags')
        )

    def tag_count(self, post):
        return post.tag_number

    tag_count.short_description = 'Number of Tags'
    tag_count.admin_order_field = 'tag_number'

    list_display = ('title', 'pub_date', 'tag_count')
    date_hierarchy = 'pub_date'
    list_filter = ('pub_date',)
    search_fields = ('title', 'text')
    """
    Making use of select_related
    under the hood, that loads the
    profile object when the post
    object is being loaded from db.
    This is an optimisation technique
    """
    list_select_related = ('profile',)
    """
    Even though the add and edit pages are different
    many of the admin options configure both pages.
    The fieldsets option, for instance, allows us to
    define which fields are available on the form
    in each page and further allow us to organize
    the fields.
    """
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'author', 'text',
            )
        }),
        ('Related', {
            'fields': (
                'tags', 'startups'
            )
        }),
    )
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('startups', 'tags')

from django.contrib import admin

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


    def tag_count(self, post):
        return post.tags.count()

    tag_count.short_description = 'Number of Tags'

    list_display = ('title', 'pub_date', 'tag_count')
    date_hierarchy = 'pub_date'
    list_filter = ('pub_date',)
    search_fields = ('title', 'text')

    # Even though the add and edit pages are different
    # many of the admin's options configure both pages.
    # The fieldsets option, for instance, allows us to
    # define which fields are available on the form
    # in each page and further allow us to organize
    # the fields.
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



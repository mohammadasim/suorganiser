from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Custom user admin for user model
    """

    def get_date_joined(self, user):
        """
        Method to get the joined date
        of the user from user profile,
        user the relationship between
        user and profile models.
        :param user:
        :return:
        """
        return user.profile.joined

    get_date_joined.short_description = 'Joined'
    get_date_joined.admin_order_field = 'profile__joined'

    def get_name(self, user):
        """
        Method to get the name
        of the user from its
        profile using the
        relationship between
        the two modules
        :param user:
        :return:
        """
        return user.profile.name

    # This sets the column name when displaying data
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'profile__name'
    # list view
    list_display = (
        'get_name',
        'email',
        'get_date_joined',
        'is_staff',
        'is_superuser'
    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'profile__joined'
    )
    search_fields = ('email',)
    ordering = ('email',)
    # The values in the below tuple
    # will become links, linking to edit
    # page for the instance of the user
    # These values come form list_display

    list_display_links = ('get_name', 'email')
    # form view
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',)}),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('Important dates', {
            'classes': ('collapse',),
            'fields': ('last_login',)
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)

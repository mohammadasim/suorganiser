from django.contrib import admin
from .models import User
from .forms import UserCreationForm


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
    # Using our own form instead of django admin form
    # for creating a new user
    # We have created this attribute
    add_form = UserCreationForm

    # override the get_form method
    def get_form(self, request, obj=None, **kwargs):
        """
        This method is overridden so that our
        UserCreationForm is used only when
        creating a new user, when updating
        an existing user, the admin app
        should use its own form
        :param request:
        :param obj:
        :param change:
        :param kwargs:
        :return:
        """
        print("The get form method has been called.")
        if obj is None:
            kwargs['form'] = self.add_form
        print(kwargs)
        return super().get_form(
            request, obj, **kwargs
        )

    # form view for user update
    # for user creation, the
    # UserCreationForm will be used

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

    # without defining this UserCreationForm was
    # being replaced
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name',
                'email',
                'password1',
                'password2'
            )
        }),
    )

    # The above works only if we apply
    # it ourselves, as the ModelAdmin
    # will not use it by default.

    def get_fieldsets(self, request, obj=None):
        """
        Overriding the default method to use
        our defined fieldsets when a new
        object is being created.
        :param request:
        :param obj:
        :return:
        """
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets()

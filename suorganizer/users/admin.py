from django.contrib import admin
from django.urls import path
from django.contrib.messages import success
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.html import escape

from .models import User, Profile
from .forms import UserCreationForm, UserChangeForm


class ProfileAdminInline(admin.StackedInline):
    """
    Class to display profile object associated
    with a user as an inline admin model
    """
    model = Profile
    can_delete = False
    exclude = ('slug',)

    def view_on_site(self, obj):
        return obj.get_absolute_url()


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
    form = UserChangeForm

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
        if obj is None:
            kwargs['form'] = self.add_form
        return super().get_form(
            request, obj, **kwargs
        )

    # form view for user update
    # for user creation, the
    # UserCreationForm will be used

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password')}),  # we added the password after creating the UserChangeForm in forms.py
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
        return super().get_fieldsets(request, obj)

    # Password Change Code
    change_password_form = AdminPasswordChangeForm
    change_user_password_template = (
        'admin/auth/user/change_password.html'
    )

    # To properly generate URL patterns for objects,
    # the admin forgoes Django convention and builds
    # the URL configuration internally in each ModelAdmin subclass
    # To add to the URL configuration, we therefore need to
    # override the get_urls() method, adding a new URL pattern to
    # the configuration generated by the ModelAdmin superclass

    def get_urls(self):
        """
        Overriding the method to add
        url pattern to the url configuration
        generated by the ModelAdmin superclass
        :return:
        """
        password_change = [
            path('<str:user_id>/password/',
                 self.admin_site.admin_view(
                     self.user_change_password
                 ),
                 name='auth_user_password_change'
                 )
        ]
        urls = super().get_urls()
        urls = password_change + urls
        return urls

    # To create the view for this URL pattern, we create
    # a method named user_change_password, which accepts
    # a request, the id of the object and a form_url keyword
    # parameter, which is meant to be passed to the template
    # context and is used as the action attribute of the HTML form tag.

    @method_decorator(sensitive_post_parameters())
    def user_change_password(self,
                             request, user_id, form_url=''):
        """
        View function for admin password change
        :param request:
        :param user_id:
        :param form_url:
        :return:
        """
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(
            request, unquote(user_id)
        )
        if user is None:
            raise Http404(
                '{name} object with primary key '
                '{key} does not exist.'.format(
                    name=force_text(
                        self.model._meta.verbose_name
                    ),
                    key=escape(user_id)
                )
            )
        if request.method == 'POST':
            # AdminPasswordChangeForm accepts a
            # user object as well
            form = self.change_password_form(
                user, request.POST
            )
            if form.is_valid():
                form.save()
                change_message = (
                    self.construct_change_message(
                        request, form, None
                    )
                )
                self.log_change(
                    request, user, change_message
                )
                success(
                    request, 'Password changed.'
                )
                update_session_auth_hash(
                    request, form.user
                )
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)
        context = {
            'title': 'Change password: {}'.format(
                escape(user.get_username())
            ),
            'form_url': form_url,
            'form': form,
            'is_popup': (
                    IS_POPUP_VAR in request.POST
                    or IS_POPUP_VAR in request.GET
            ),
            'opts': self.model._meta,
            'original': user,
        }
        context.update(
            admin.site.each_context(request)
        )
        request.current_app = self.admin_site.name
        return TemplateResponse(
            request,
            self.change_user_password_template,
            context
        )

    def get_inline_instances(self, request, obj=None):
        """
        Overriding the method to display
        inline only if a user object is
        passed to the method
        :param request:
        :param obj:
        :return:
        """
        if obj is None:
            return tuple()
        inline_instance = ProfileAdminInline(
            self.model, self.admin_site
        )
        return (inline_instance,)

    # Adding actions

    # Registering actions that we create
    actions = ['make_staff', 'remove_staff']

    # Defining action
    def make_staff(self, request, queryset):
        """
        Make a list of users staff
        :param request:
        :param queryset:
        :return:
        """
        rows_updated = queryset.update(
            is_staff=True
        )
        if rows_updated == 1:
            message = '1 user was'
        else:
            message = '{} users were'.format(rows_updated)
        message += ' successfully made staff'
        self.message_user(request, message)

    make_staff.short_description = (
        'Allow user to access Admin Site.'
    )

    def remove_staff(self, request, queryset):
        """
        Method to withdraw staff status from
        users
        :param request:
        :param queryset:
        :return:
        """
        row_updated = queryset.update(
            is_staff=False
        )
        if row_updated == 1:
            message = '1 user was'
        else:
            message = '{} users were'.format(row_updated)
        message += ' removed from staff list.'
        self.message_user(request, message)

    remove_staff.short_description = (
        'Stop user access to Admin Site.'
    )

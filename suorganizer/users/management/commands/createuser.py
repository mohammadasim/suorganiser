import sys
import getpass
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError
)
from django.utils.encoding import smart_str
from django.utils.text import slugify, capfirst
from users.models import Profile


class Command(BaseCommand):
    """
    Command class is required to
    create a custom management command
    """
    help = 'Create a new User with Profile'
    required_error = (
        'You must user --{} with --noinput.'
    )

    def __init__(self, *args, **kwargs):
        """
        Overriding the method so we can
        add commonly accessed pieces of
        data as class attributes.
        :param args:
        :param kwargs:
        """
        super().__init__(self, *args, **kwargs)
        self.user = get_user_model()
        self.name_field = Profile._meta.get_field('name')
        # The USERNAME_FIELD in User model is set to email
        self.username_field = (
            self.user._meta.get_field(self.user.USERNAME_FIELD)
        )

    def execute(self, *args, **options):
        """
        This method is internall used
        by the Command class to run the
        command.
        We override it to just grab the
        stdin keyword arg, as we will
        use it in the interactive mode
        to make sure we can actually
        behave interactively.
        :param args:
        :param options:
        :return:
        """
        self.stdin = options.get(
            'stdin', sys.stdin
        )
        return super().execute(*args, **options)

    def add_arguments(self, parser):
        """
        Method that will receive the
        command line arguments passed
        by the user.
        This method will receive these
        arguments from the Command class.
        :param parser:
        :return:
        """
        parser.add_argument(
            '--{}'.format(self.name_field.name),
            dest=self.name_field.name,
            default=None,
            help='User Profile name.'
        )
        parser.add_argument(
            '--{}'.format(self.user.USERNAME_FIELD),
            dest=self.user.USERNAME_FIELD,
            default=None,
            help='User login.'
        )
        # The interactive attribute of the object
        # created and returned by the parser is
        # a little different from other attributes.
        # The default of this argument is True, but
        # if the flag --noinput is specified, the
        # action value 'store_false' tells the
        # argumentParser to change the interactive
        # value to False.
        parser.add_argument(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='DO NOT prompt the user for '
                 'input of any kind. You must use '
                 '--{} with --noinput, along with '
                 'an option for any other '
                 'required field. Users created '
                 'with --noinput will not be able '
                 'to login unitil they\'re given '
                 'a valid password.'.format(
                self.user.USERNAME_FIELD
            )
        )

    def check_unique(self, model, field, value, halt=True):
        """
        Helper method to check if the value
        passed by the user already exists
        in the database or not
        :param model:
        :param field:
        :param value:
        :param halt:
        :return:
        """
        try:
            q = '{}__iexact'.format(field.name)
            filter_dict = {q: value}
            model.objects.get(**filter_dict)
        except ObjectDoesNotExist:
            # when object doesn't exist
            # we return the value, because
            # it means that the value provided
            # is unique
            return value
        else:
            if halt:
                raise CommandError(
                    'That {} is already taken'
                        .format(
                        capfirst(
                            field.verbose_name
                        )
                    )
                )
            else:
                self.stderr.write(
                    'Error: That {} is '
                    'already taken.'.format(
                        capfirst(field.verbose_name)
                    )
                )
        return None

    def handle_none_interactive(self, name, username, **options):
        """
        Method to handle non interactive
        mode of user creation management command
        :param name:
        :param username:
        :param options:
        :return:
        """
        if not username:
            raise CommandError(
                self.required_error.format(
                    self.user.USERNAME_FIELD
                )
            )
        if not name:
            raise CommandError(
                self.required_error.format(
                    self.name_field.name
                )
            )
        username = self.check_unique(
            self.user,
            self.username_field,
            username
        )
        name = self.check_unique(
            Profile,
            self.name_field,
            name
        )
        return (name, username)

    def get_field_interactive(self, model, field):
        """
        Method to prompt user for input
        and verify that the input is correct
        :param model:
        :param field:
        :return:
        """
        value = None
        input_msg = '{}: '.format(
            capfirst(field.verbose_name)
        )
        # Until the input is correct
        # (value is no longer None)
        # we continue to show the prompt
        # to the user
        while value is None:
            # we use the python builtin input function
            # it shows the input_msg by writing to the
            # standard output without a trailing new line
            # It then reads a line form input converts it
            # into string, stripping trailing new line
            # and returns that.
            value = input(input_msg)
            value = self.check_unique(
                model, field, value, halt=False
            )
            if not value:
                # if value is none
                # go back to the start of the loop
                continue
            return value

    def handle_interactive(self, name, username, **options):
        """
        Method to create user interactively
        :param name: 
        :param username: 
        :param options: 
        :return: 
        """
        password = None
        # First we need to make sure  that we 
        # can behave, interactively. Using the
        # stdin attribute that we assigned in
        # execute() we check that the management
        # command is being called from an 
        # interactive shell. If not we raise a
        # commanderror
        if (hasattr(self.stdin, 'isatty')
                and not self.stdin.isatty()):
            self.stdout.write(
                'User creation skipped due to '
                'not running in a TTY. '
                'You can run manage.py createuser '
                'in your project to createone '
                'manually.'
            )
            sys.exit(1)
            # We check the username and name
            # arguments as it is possible for
            # createuser to be called with
            # certain parameters set
            # noninteractively.

        if username is not None:
            username = self.check_unique(
                self.user,
                self.username_field,
                username,
                halt=False
            )
        if name is not None:
            name = self.check_unique(
                Profile, self.name_field, name, halt=False
            )

        try:
            # no we ask for the parameters interactively
            # if they have not been passed already
            if not username:
                username = (
                    self.get_field_interactive(
                        self.user,
                        self.username_field
                    )
                )
            if not name:
                name = (
                    self.get_field_interactive(
                        Profile,
                        self.name_field
                    )
                )
            while password is None:
                password = getpass.getpass()
                password2 = getpass.getpass(
                    # smart_str shows the message and takes the password input
                    smart_str(
                        'Password (again): '
                    )
                )
                if password != password2:
                    self.stderr.write(
                        'Error: Your '
                        'passwords did not match'
                    )
                    password = None
                    continue
                    # strip returns copy of string
                    # with leading and trailing
                    # whitespace remove.
                if password.strip() == '':
                    self.stderr.write(
                        'Error: Blank password '
                        'are not allowed'
                    )
                    password = None
                    continue
            return (name, username, password)

        except KeyboardInterrupt:
            self.stderr.write(
                '\nOperation cancelled'
            )
            sys.exit(1)

    def create_user(self, name, username, password):
        """
        Method to create user, we use
        the create_user method defined
        in the custom user manager class
        UserManager.
        :param name:
        :param username:
        :param password:
        :return:
        """
        new_user = self.user.objects.create_user(
            email=username, password=password
        )
        # We use try catch because slugify of words
        # like super man and super-man will result
        # in similar word super-man, but they
        # can be returned as unique by our unique
        # method
        try:
            Profile.objects.create(
                user=new_user,
                name=name,
                slug=slugify(name)
            )
        except Exception as e:
            raise CommandError(
                'Could  not create Profile:\n{}'
                    .format('; '.join(e.message))
            )

    def handle(self, **options):
        """
        This is the main method that
        will be executed when the management
        command createuser is run by the
        user
        :param options:
        :return:
        """
        name = options.pop(
            self.name_field.name, None
        )
        username = options.pop(
            self.user.USERNAME_FIELD, None
        )
        password = None

        # We check if we are in
        # interactive mode or not
        # by checking the value
        # passed to interactive
        # variable
        if not options['interactive']:
            name, username = (
                self.handle_non_interactive(
                    name, username, **options
                )
            )
        else:
            name, username, password = (
                self.handle_interactive(
                    name, username, **options
                )
            )
        self.create_user(name, username, password)

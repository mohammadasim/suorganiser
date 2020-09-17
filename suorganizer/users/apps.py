from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        """
        Overriding the ready method,
        so that our signals.py module
        is also loaded when the app is
        being loaded.
        :return:
        """
        import users.signals

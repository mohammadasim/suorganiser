"""
Django does not know by default to
load apps.py, we tell it to do so
by setting the default_app_config
variable in our package's init
module
"""
default_app_config = 'users.apps.UserConfig'

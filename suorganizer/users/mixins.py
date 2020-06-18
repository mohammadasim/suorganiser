"""
Module containing mixin for the users app
"""
import logging
import traceback
from logging import CRITICAL, ERROR
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import \
    urlsafe_base64_encode

logger = logging.getLogger(__name__)


class ActivationMailFormMixin:
    """
    A class to provide sending an account activation
    email functionality to both CreateAccount
    and ActivateAccount views. Both views deal with
    new user
    In this class the _mail_sent private attribute
    has a value True or False, depending on whether
    an email was sent or not.
    """
    mail_validation_error = ''

    def log_mail_error(self, **kwargs):
        """
        Method to log problems in the class
        :param kwargs:
        :return:
        """
        msg_list = [
            'Activation email did not send. \n',
            'from_email: {from_email}\n',
            'subject: {subject}\n',
            'message: {message}\n'
        ]
        recipient_list = kwargs.get(
            'recipient_list, []'
        )
        for recipient in recipient_list:
            msg_list.insert(1, 'recipient: {r}\n'.format(
                r=recipient
            ))
        if 'error' in kwargs:
            level = ERROR
            error_msg = (
                'error: {0.__class__.__name__}\n'
                'args: {0.args}\n'
            )
            error_info = error_msg.format(
                kwargs['error']
            )
            msg_list.insert(1, error_info)
        else:
            level = CRITICAL
        # change the list into string
        msg = ''.join(msg_list).format(**kwargs)
        logger.log(level, msg)

    @property
    def mail_sent(self):
        """
        Getter method for the private attribute
        _mail_sent
        :return:
        """
        if hasattr(self, '_mail_sent'):
            return self._mail_sent
        return False

    @mail_sent.setter
    def set_mail_sent(self, value):
        """
        Setter method for _mail_sent
        Raises TypeError as this attribute
        cannot be set by user
        :param value:
        :return:
        """
        raise TypeError('Cannot set mail_sent attribute.')

    def get_message(self, **kwargs):
        """
        Method to get the message template, populate its variables
        and render it like a string.
        :param kwargs:
        :return:
        """
        email_template_name = kwargs.get('email_template_name')
        context = kwargs.get('context')
        # render_to_string loads a template like get_template()
        # and calls its render() method immediately. It takes
        # template name, context, request and using as argument
        return render_to_string(email_template_name, context)

    def get_subject(self, **kwargs):
        """
        Method to get the subject template, replace
        the template variables with their values
        and return it as a string
        :param kwargs:
        :return:
        """
        subject_template_name = kwargs.get('subject_template_name')
        context = kwargs.get('context')
        subject = render_to_string(subject_template_name, context)
        # subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        return subject

    def get_context_data(self, request, user, context=None):
        if context is None:
            context = dict()
        current_site = get_current_site(request)
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )
        context.update({
            'domain': current_site.domain,
            'protocol': protocol,
            'site_name': current_site.name,
            'token': token,
            'uid': uid,
            'user': user
        })
        return context

    def _send_mail(self, request, user, **kwargs):
        """
        Private method for sending mail
        :param request:
        :param user:
        :param kwargs:
        :return:
        """
        kwargs['context'] = self.get_context_data(request, user)
        mail_kwargs = {
            'subject': self.get_subject(**kwargs),
            'message': self.get_message(**kwargs),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': [user.email]
        }
        try:
            # number_sent will be 0 or 1
            number_sent = send_mail(**mail_kwargs)
        except Exception as error:
            self.log_mail_error(
                error=error, **mail_kwargs
            )
            if isinstance(error, BadHeaderError):
                err_code = 'badHeader'
            elif isinstance(error, SMTPException):
                err_code = 'smtperror'
            else:
                err_code = 'unexpectederror'
            return False, err_code
        else:
            if number_sent > 0:
                return True, None
            self.log_mail_error(
                request, user, **kwargs
            )
            return False, 'unknownerror'

    def send_mail(self, user, **kwargs):
        """
        A public method to be called by
        developers for sending email
        :param user:
        :param kwargs:
        :return:
        """
        request = kwargs.pop('request', None)
        if request is None:
            tb = traceback.format_stack()
            tb = [' ' + line for line in tb]
            logger.warning(
                'send_mail called without '
                'request.\nTraceback:\n{}'.format(
                    ''.join(tb)
                )
            )
            # Below we are setting the private variable
            self._mail_sent = False
            # In the following statement rather than returning
            # the private variable directly, the get method for
            # the private variable is used to return its value
            return self.mail_sent
        # the private method is called to send the email.
        self._mail_sent, error = (
            self._send_mail(request, user, **kwargs)
        )
        # if for whatever reason the mail is not sent
        # and the method returns False
        if not self.mail_sent:
            self.add_error(
                None,  # no field - form error
                ValidationError(
                    self.mail_validation_error,
                    code=error
                )
            )
        return self.mail_sent


class MailContextViewMixin:
    """
    Views will inherit this class.
    The function of this class is to
    provide the kwargs to the send_mail
    method, so that we don't have to remember them.
    """
    email_template_name = 'users/email_create.txt'
    subject_template_name = 'users/subject_create.txt'

    def get_save_kwargs(self, request):
        """
        Method to build a dictionary with the
        keyword arguments that send_mail method
        expects
        :param request:
        :return:
        """
        return {
            'email_template_name':
                self.email_template_name,
            'request': request,
            'subject_template_name':
                self.subject_template_name
        }

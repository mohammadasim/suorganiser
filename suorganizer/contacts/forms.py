from django.core.exceptions import ValidationError
from django.core.mail import mail_managers, BadHeaderError
from django.forms import forms


class ContactForm(forms.Form):
    FEEDBACK = 'F'
    CORRECTION = 'C'
    SUPPORT = 'S'
    REASON_CHOICES = (
        (FEEDBACK, 'feedback'),
        (CORRECTION, 'Correction'),
        (SUPPORT, 'Support'),
    )
    email = forms.EmailField(
        initial='youremail@domain.com')
    text = forms.CharField(widget=forms.Textarea)
    reason = forms.ChoiceField(
        choices=REASON_CHOICES,
        initial=FEEDBACK
    )

    def send_mail(self):
        reason = self.cleaned_data.get('reason')
        reason_dict = dict(self.REASON_CHOICES)
        full_reason = reason_dict.get(reason)
        email = self.cleaned_data.get('email')
        text = self.cleaned_data.get('text')
        body = 'Message From: {}\n\n{}\n'.format(
            email, text
        )
        try:
            # shortcut for send_mail
            mail_managers(full_reason, body)
        except BadHeaderError:
            self.add_error(
                None,
                ValidationError(
                'Could Not Send Email.\n'
                'Extra Headers not allowed'
                'in email body.',
                code='badheader'
            ))
            return False
        else:
            return True
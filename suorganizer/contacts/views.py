from django.contrib.messages import success
from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm


class ContactView(View):
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'

    def get(self, request):
        return render(request,
                      self.template_name,
                      {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            send_email = bound_form.send_mail()
            if send_email:
                success(
                    request,
                    'Email successfully sent.'
                )
                return redirect('blogs_posts_list')
        else:
            return render(request,
                          self.template_name,
                          {'form': bound_form})

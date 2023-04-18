from allauth.account.adapter import DefaultAccountAdapter
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        context = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
        }
        subject = render_to_string(
            "account/email/email_confirmation_subject.txt", context
        )
        subject = "".join(subject.splitlines())
        message = render_to_string(
            "account/email/email_confirmation_message.txt", context
        )
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [emailconfirmation.email_address.email])

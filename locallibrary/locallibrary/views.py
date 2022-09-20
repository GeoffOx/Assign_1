from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import logging


def password_reset_request(request):
    logging.warning('In the password_reset_request')
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = 'Reset password'
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        'email': user.email,
                        'domain': 'gochsner.pythonanywhere.com',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    message = render_to_string(email_template_name, c)
                    # user = request.user  # request was passed to the method as a parameter for the view
                    user_email = user.email  # pull user’s email out of the user record
                    # try to send the e-mail – note you can send to multiple users – this just sends
                    # to one user.
                    try:
                        send_mail(subject, message, 'geoff.unomaha@gmail.com', [user_email], False, 'geoff.unomaha@gmail.com', 'psdtispxdfhkzrxe')
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    return redirect("/accounts/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html",
                  context={"password_reset_form": password_reset_form})

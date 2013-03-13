# -*- encoding: utf-8 -*-
#
# profiles/views.py: Profile management views.
#
# This file is part of mentors.debian.net
#
# Copyright © 2013 Nicolas Dandrimont
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#

from django.contrib.auth import login

from le_social.registration import views

from .forms import UserCreationForm
from .models import MentorsUser


class Register(views.Register):
    form_class = UserCreationForm
    template_name = "profiles/registration/register.html"
    notification_subject_template_name = "profiles/registration/activation_email_subject.txt"
    notification_template_name = "profiles/registration/activation_email.txt"

    def form_valid(self, form):
        ret = super(Register, self).form_valid(form)
        self.user.is_active = False
        self.user.save()
        return ret


class RegistrationComplete(views.RegistrationComplete):
    template_name = "profiles/registration/registration_complete.html"


class RegistrationClosed(views.RegistrationClosed):
    template_name = "profiles/registration/registration_closed.html"


class Activate(views.Activate):
    template_name = "profiles/registration/activate.html"

    def activate(self):
        user = MentorsUser.objects.get(pk=self.activation_key)
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)


class ActivationComplete(views.ActivationComplete):
    template_name = "profiles/registration/activation_complete.html"


register = Register.as_view()
registration_complete = RegistrationComplete.as_view()
registration_closed = RegistrationClosed.as_view()

activate = Activate.as_view()
activation_complete = ActivationComplete.as_view()

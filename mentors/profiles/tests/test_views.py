# -*- encoding: utf-8 -*-
#
# profiles/test/test_views.py: User Profile related view tests
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

from __future__ import unicode_literals

import os

from django.core import mail
from django.core.urlresolvers import reverse

from lib.test import TestCase
from profiles.models import GPGKey, MentorsUser


class RegistrationProcessTests(TestCase):
    def test_registration_process(self):
        user_data = {
            'email': 'test.registration.process@example.com',
            'full_name': 'Test R. Process',
            'password1': 'verysecurepassword',
            'password2': 'verysecurepassword',
        }

        # Check contents of the registration page
        response = self.client.get(reverse("registration_register"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Register")
        self.assertContains(response, "Submit")

        # Try registering
        response = self.client.post(reverse("registration_register"), data=user_data)
        self.assertRedirects(response, reverse("registration_complete"))

        # Check that the user was created and is inactive
        self.assertFalse(MentorsUser.objects.get(email=user_data["email"]).is_active)

        # Check that we sent the activation mail to the right person
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("activate", mail.outbox[0].subject)
        self.assertIn(user_data["email"], mail.outbox[0].to)
        self.assertIn(user_data["full_name"], mail.outbox[0].body)

        # Retrieve the activation link
        for line in mail.outbox[0].body.splitlines():
            if line.startswith("http://testserver/"):
                url = line[len("http://testserver"):].strip()
                break
        else:
            self.fail("email does not contain activation link!")

        # And test it
        response = self.client.get(url)
        self.assertRedirects(response, reverse("registration_activation_complete"))
        self.assertTrue(MentorsUser.objects.get(email=user_data["email"]).is_active)

class ViewProfileTests(TestCase):
    #flake8: noqa
    def setUp(self):
        self.user = MentorsUser.objects.create()
        self.user.email = "nicolas.dandrimont@crans.org"
        self.user.full_name = "Nicolas Dandrimont"
        self.user.set_password("test_pwd")
        self.user.is_active = True
        self.user.save()

        nicolas_key_path = os.path.join(os.path.dirname(__file__), 'data', 'dandrimont.asc')
        self.nicolas_key = file(nicolas_key_path).read()
        self.nicolas_key_fingerprint = '791F12396630DD71FD364375B8E5087766475AAF'
        self.nicolas_key_algorithm = '4096R'

        key = GPGKey(owner=self.user, key=self.nicolas_key)
        key.save()

    def test_info_display(self):
        response = self.client.get(reverse("profile_view", args=[self.user.email]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.full_name)
        self.assertContains(response, self.nicolas_key_fingerprint)
        self.assertContains(response, self.nicolas_key_algorithm)

    def test_wrong_user_display(self):
        response = self.client.get(reverse("profile_view", args=["random@example.com"]))

        self.assertEqual(response.status_code, 404)

    def test_display_edit_link(self):
        self.client.login(username="nicolas.dandrimont@crans.org", password="test_pwd")
        response = self.client.get(reverse("profile_view", args=[self.user.email]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("profile_edit"))

class EditProfileTests(TestCase):
    #flake8: noqa
    def setUp(self):
        self.user = MentorsUser.objects.create()
        self.user.email = "nicolas.dandrimont@crans.org"
        self.user.full_name = "Nicolas Dandrimont"
        self.user.set_password("test_pwd")
        self.user.is_active = True
        self.user.save()

        self.nicolas_key_path = os.path.join(os.path.dirname(__file__), 'data', 'dandrimont.asc')
        self.nicolas_key_fingerprint = '791F12396630DD71FD364375B8E5087766475AAF'
        self.nicolas_key_algorithm = '4096R'

    def test_edit_logged_out(self):
        response = self.client.get(reverse("profile_edit"))
        self.assertRedirects(response, reverse("login") + '?next=%s' % reverse('profile_edit'))

    def test_edit_display(self):
        self.client.login(username="nicolas.dandrimont@crans.org", password="test_pwd")
        response = self.client.get(reverse("profile_edit"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.full_name)
        self.assertContains(response, self.nicolas_key_fingerprint[-16:])
        self.assertContains(response, self.nicolas_key_algorithm)

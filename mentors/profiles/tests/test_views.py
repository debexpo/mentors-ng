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

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase


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

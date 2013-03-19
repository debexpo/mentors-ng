# -*- encoding: utf-8 -*-
#
# profiles/test/test_forms.py: User Profile related form tests
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

from lib.test import TestCase
from profiles.forms import UserCreationForm


class UserCreationFormTests(TestCase):
    def test_different_passwords(self):
        data = {
            'email': 'test@example.com',
            'password1': 'test1',
            'password2': 'test2',
        }

        form = UserCreationForm(data=data)

        self.assertFalse(form.is_valid())

    def test_form_save(self):
        data = {
            'email': 'test@example.com',
            'full_name': "Full Name Test",
            'password1': 'password',
            'password2': 'password',
        }

        form = UserCreationForm(data=data)

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.full_name, data['full_name'])
        self.assertTrue(user.check_password(data['password2']))

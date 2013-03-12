# -*- encoding: utf-8 -*-
#
# profiles/test/test_models.py: User Profile related model tests
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

from django.test import TestCase

from profiles.models import MentorsUser


class MentorsUserTests(TestCase):
    # flake8: noqa
    def setUp(self):
        user = MentorsUser.objects.create_user('user@example.com')
        super_user = MentorsUser.objects.create_superuser('superuser@example.com')

        user.full_name = "Normal User"
        user.save()

        super_user.full_name = "Super User"
        super_user.save()

    def test_user_short_name(self):
        user = MentorsUser.objects.all()[0]
        self.assertIn(user.email, user.get_short_name())

    def test_user_full_name(self):
        user = MentorsUser.objects.all()[0]
        self.assertIn(user.email, user.get_full_name())
        self.assertIn(user.full_name, user.get_full_name())

    def test_user_unicode(self):
        user = MentorsUser.objects.all()[0]
        self.assertIn(user.email, unicode(user))

    def test_user_create_empty_email(self):
        with self.assertRaises(ValueError):
            MentorsUser.objects.create_user('')

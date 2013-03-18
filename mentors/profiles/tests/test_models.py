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

import os

from django.conf import settings

from lib.test import TestCase
from lib.gnupg import GnuPG
from profiles.models import GPGKey, MentorsUser


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


class GPGKeyTests(TestCase):
    #flake8: noqa
    def setUp(self):
        self.nicolas = MentorsUser.objects.create_user('nicolas@dandrimont.eu')
        self.nicolas.save()
        self.clement = MentorsUser.objects.create_user('clement@mux.me')
        self.clement.save()
        self.random = MentorsUser.objects.create_user('whomever@example.com')
        self.random.save()

        nicolas_key_path = os.path.join(os.path.dirname(__file__), 'data', 'dandrimont.asc')
        self.nicolas_key = file(nicolas_key_path).read()
        self.nicolas_key_fingerprint = '791F12396630DD71FD364375B8E5087766475AAF'
        self.nicolas_key_algorithm = '4096R'

        clement_key_path = os.path.join(os.path.dirname(__file__), 'data', 'schreiner.asc')
        self.clement_key = file(clement_key_path).read()
        self.clement_key_fingerprint = 'E4BA6F4097B08D5AE8DC68C95E39E0E38123F27C'
        self.clement_key_algorithm = '4096R'

    def test_gpg_right_user(self):
        new_key = GPGKey(owner=self.nicolas)
        new_key.key = self.nicolas_key
        new_key.save()

        self.assertEquals(new_key.fingerprint, self.nicolas_key_fingerprint)
        self.assertEquals(new_key.algorithm, self.nicolas_key_algorithm)

    def test_gpg_wrong_user(self):
        from django.core.exceptions import ValidationError

        new_key = GPGKey(owner=self.random)
        new_key.key = self.nicolas_key
        with self.assertRaises(ValidationError):
            new_key.save()

    def test_gpg_wrong_data(self):
        from django.core.exceptions import ValidationError

        new_key = GPGKey(owner=self.random)
        new_key.key = "blablablablabla"
        with self.assertRaises(ValidationError):
            new_key.save()

    def test_gpg_display(self):
        new_key = GPGKey(owner=self.nicolas)
        new_key.key = self.nicolas_key
        new_key.save()

        self.assertIn(new_key.algorithm, unicode(new_key))
        self.assertIn(new_key.fingerprint[-16:], unicode(new_key))

    def test_gpg_keyring(self):
        nicolas_key = GPGKey(owner=self.nicolas)
        nicolas_key.key = self.nicolas_key
        nicolas_key.save()

        clement_key = GPGKey(owner=self.clement)
        clement_key.key = self.clement_key
        clement_key.save()

        keyring_path = os.path.join(settings.MENTORS_ROOT, 'gpg/pubring.gpg')
        self.assertTrue(os.path.exists(keyring_path))

        gpg = GnuPG(default_keyring=keyring_path)

        keys = list(gpg.list_keys())
        self.assertEqual(len(keys), 2)

        fprs = [key.key.fingerprint for key in keys]
        self.assertIn(self.nicolas_key_fingerprint, fprs)
        self.assertIn(self.clement_key_fingerprint, fprs)

        clement_key.delete()

        keys = list(gpg.list_keys())
        self.assertEqual(len(keys), 1)

        fprs = [key.key.fingerprint for key in keys]
        self.assertIn(self.nicolas_key_fingerprint, fprs)

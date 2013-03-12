# -*- encoding: utf-8 -*-
#
# profiles/models.py: User Profile related models
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

from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class MentorsUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """Create and saves a User with the given email and password."""

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=MentorsUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class MentorsUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_("email address"), max_length=255, unique=True, db_index=True)
    full_name = models.CharField(verbose_name=_("full name"), max_length=512, blank=True)

    USERNAME_FIELD = 'email'

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MentorsUserManager()

    def get_full_name(self):
        return "%s <%s>" % (self.full_name, self.email)

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email


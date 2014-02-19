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

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from lib.utils import get_gnupg
from lib.gnupg import GpgInvalidKeyBlock


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

    def get_absolute_url(self):
        return reverse('profile_view', args=[self.email])

    def __unicode__(self):
        return self.email


class GPGKey(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="gpg_keys")
    key = models.TextField(verbose_name=_('key contents'), blank=False)
    algorithm = models.CharField(max_length=10)
    fingerprint = models.CharField(max_length=128, unique=True)

    def __init__(self, *args, **kwargs):
        super(GPGKey, self).__init__(*args, **kwargs)
        self.gpg = get_gnupg()

    def as_key_block(self):
        from django.core.exceptions import ValidationError
        if not hasattr(self, '__key_block'):
            try:
                self.__key_block = self.gpg.parse_key_block(data=self.key)
            except GpgInvalidKeyBlock:
                raise ValidationError(_('The given key data is invalid'))
        return self.__key_block

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.as_key_block().key is None:
            raise ValidationError(_('The given key data is invalid'))

        for name, email in self.as_key_block().user_ids:
            if email == self.owner.email:
                break
        else:
            raise ValidationError(_('The given key does not belong to the user'))

        self.fingerprint = self.as_key_block().key.fingerprint
        self.algorithm = "%(strength)s%(type)s" % (self.as_key_block().key._asdict())

    def save(self, *args, **kwargs):
        self.clean()
        self.gpg.add_key(data=self.key)
        return super(GPGKey, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.gpg.remove_key(self.fingerprint)
        return super(GPGKey, self).delete(*args, **kwargs)

    def __unicode__(self):
        return "%(algorithm)s/%(fingerprint)s" % self.__dict__

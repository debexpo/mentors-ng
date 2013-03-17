# -*- encoding: utf-8 -*-
#
# profiles/forms.py: Profile management forms.
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

from django import forms
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from extra_views import InlineFormSet

from lib.utils import gpg
from .models import MentorsUser, GPGKey


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MentorsUser
        fields = ('email', 'full_name')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserModificationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    old_password = forms.CharField(label='Current password', widget=forms.PasswordInput, required=False)
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = MentorsUser
        fields = ('full_name',)

    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.user = user
        super(UserModificationForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        # Check that the given password matches the current one
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self._raw_value("new_password1")
        new_password2 = self._raw_value("new_password2")
        if new_password1 and new_password2 and not (old_password and self.user.check_password(old_password)):
            raise forms.ValidationError("Old password does not match")
        return old_password

    def clean_new_password2(self):
        # Check that the two password entries match
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("New passwords don't match")
        return new_password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserModificationForm, self).save(commit=False)
        if self.cleaned_data["new_password1"]:
            user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user


class GPGKeyInputWidget(forms.FileInput):
    def render(self, name, value, attrs=None):
        if value:
            key = gpg.parse_key_block(value).key
            return mark_safe("<div>Existing key: %(key)s</div>" % {'key': "%s%s/%s" % (key.strength, key.type, key.fingerprint[-16:])})
        else:
            return super(GPGKeyInputWidget, self).render(name, None, attrs)

    def value_from_datadict(self, data, files, name):
        value = files.get(name)
        if value:
            val = value.read()
            value.seek(0)
            return val
        else:
            return None


class GPGKeyUploadForm(forms.ModelForm):
    """A form to allow upload of a GPG key"""
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False

        super(GPGKeyUploadForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GPGKey
        fields = ('key',)
        widgets = {'key': GPGKeyInputWidget()}


class InlineGPGKeyFormSet(InlineFormSet):
    model = GPGKey
    extra = 1
    form_class = GPGKeyUploadForm

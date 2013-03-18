# -*- encoding: utf-8 -*-
#
# lib/test.py: testing utilities
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

import shutil
import tempfile

import django.test as djtest
from django.test.utils import override_settings


class OverrideMentorsRoot(override_settings):
    def __init__(self, **kwargs):
        super(OverrideMentorsRoot, self).__init__(**kwargs)
        self.tempdir = None

    def enable(self):
        self.tempdir = tempfile.mkdtemp()
        self.options['MENTORS_ROOT'] = self.tempdir
        super(OverrideMentorsRoot, self).enable()

    def disable(self):
        super(OverrideMentorsRoot, self).disable()
        shutil.rmtree(self.tempdir)
        del self.options['MENTORS_ROOT']
        self.tempdir = None


@OverrideMentorsRoot()
class TestCase(djtest.TestCase):
    """A mentors-specific testcase, setting the data directory to a separate directory"""
    pass

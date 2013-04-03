# -*- encoding: utf-8 -*-
#
# repository/test/test_models.py: Repository related model tests
#
# This file is part of mentors.debian.net
#
# Copyright © 2013 Clément Schreiner
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

from repository.models import Package, PackageUpload, BinaryPackage, SourcePackage, PackageFile

class PackageTests(TestCase):
    #flake8: noqa
    pass


class PackageUploadTests(TestCase):
    #flake8: noqa
    pass


class BinaryPackageTests(TestCase):
    #flake8: noqa
    pass


class SourcePackageTests(TestCase):
    #flake8: noqa
    pass


class PackageFileTests(TestCase):
    #flake8: noqa
    pass


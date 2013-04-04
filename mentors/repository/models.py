# -*- encoding: utf-8 -*-
#
# repository/models.py: Repository related models
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

from django.db import models
from django.conf import settings

class Package(models.Model):
    name = models.TextField()
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL)
    version = models.TextField()
    maintainer = models.TextField()
    section = models.TextField()
    suite = models.ForeignKey(Suite)
    description = models.TextField()
    qa_status = models.IntegerField()
    component = models.TextField()
    priority = models.TextField()
    closes = models.TextField()
    upload_time = models.DateTimeField()

    def __unicode__(self):
        return '{0}-{1} in {2} (by {3})'.format(self.name,
                                                self.version,
                                                self.suite,
                                                self.uploader)


class BinaryPackage(models.Model):
    name = models.TextField()
    package = models.ForeignKey(Package)
    arch = models.TextField()
    description = models.TextField()

    def __unicode__(self):
        return '{0} ({1})'.format(self.name,
                                  self.arch)



class SourcePackage(models.Model):
    name = models.TextField()
    package = models.ForeignKey(PackageUpload)

    def __unicode__(self):
        return self.name


class PackageFile(models.Model):
    binary = models.ForeignKey(BinaryPackage)
    source = models.ForeignKey(SourcePackage)
    filename = models.TextField()
    size = models.IntegerField()
    checksum = models.CharField(max_length=200)

    def __unicode__(self):
        return '{0} ({1})'.format(self.filename,
                                  self.binary if self.binary else self.source)


class Suite(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

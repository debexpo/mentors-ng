# -*- encoding: utf-8 -*-
#
# lib/utils.py: "site-wide" utilities
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

import os

from django.conf import settings

from . import gnupg

# Provide a singleton instance of the GnuPG object
if not hasattr(gnupg, 'gnupg_instance'):
    gpg_dir = os.path.join(settings.MENTORS_ROOT, 'gpg')
    if not os.path.exists(gpg_dir):
        os.makedirs(gpg_dir)
    pubring = os.path.join(gpg_dir, 'pubring.gpg')
    gnupg.gnupg_instance = gnupg.GnuPG(default_keyring=pubring)

gpg = gnupg.gnupg_instance

# -*- encoding: utf-8 -*-
#
# Makefile: Useful commands to run on the mentors project.
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

.PHONY: test
test:
	cd mentors; coverage run --source=. manage.py test --settings=mentors.settings.test; coverage html --omit=*/migrations/*

.PHONY: flake8
flake8:
	flake8 --exclude=migrations --max-line-length=160 $(CURDIR)

.PHONY: docs
docs:
	make -C docs html

.PHONY: distclean
distclean:
	rm -rf mentors/.coverage mentors/htmlcov docs/_build

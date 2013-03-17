# -*- encoding: utf-8 -*-
#
# profiles/urls.py: Profile management urls.
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

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',

    url(r'^activate/complete/$', views.activation_complete, name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>[^/]+)/$', views.activate, name='registration_activate'),

    url(r'^register/$', views.register, name='registration_register'),
    url(r'^register/complete/$', views.registration_complete, name='registration_complete'),
    url(r'^register/closed/$', views.registration_closed, name='registration_closed'),

    url(r'^view/(?P<email>[^/]+)/$', views.profile_view, name='profile_view'),
)

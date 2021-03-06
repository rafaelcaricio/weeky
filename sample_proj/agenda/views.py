#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Weeky
# https://github.com/rafaelcaricio/weeky
#
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from agenda.forms import MyTestForm

def mytestview(request):
    if request.method == 'POST':
        form = MyTestForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            plan = form.cleaned_data['plan']
            for key in plan.iterkeys():
                print key, plan[key]
            return HttpResponseRedirect('/mythanks/')
    else:
        form = MyTestForm()
    return TemplateResponse(request, 'mytest.html', {'form' : form,})


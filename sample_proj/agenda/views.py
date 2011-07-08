#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

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
    return render_to_response('mytest.html', {'form' : form,})


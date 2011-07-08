#!/usr/bin/env python
# -*- coding: utf-8 -*-

from agenda.forms import MyTestForm

def mytestview(request):
    if request.method == 'POST':
        form = MyTestForm(request.POST)
        if form.is_valid():
    else:
        user = form.cleaned_data[‘user’]
        plan = form.cleaned_data[‘plan’]
        for key in plan.viewkeys():
            print plan[key]
        return HttpResponseRedirect(‘/mythanks/’)
    form = MyTestForm()
    return render_to_response(‘mytest.html’, {‘form’ : form,})


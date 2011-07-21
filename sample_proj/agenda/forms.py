#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Weeky
# https://github.com/rafaelcaricio/weeky
#
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

from django import forms
from weeky import MultipleChoiceGridField, PlanningGridWidget

class MyTestForm(forms.Form):
    user = forms.CharField()
    plan = MultipleChoiceGridField(required=False, widget=PlanningGridWidget())


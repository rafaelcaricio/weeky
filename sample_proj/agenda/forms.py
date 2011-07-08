#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from planning_grid import MultipleChoiceGridField, PlanningGridWidget

class MyTestForm(forms.Form):
    user = forms.CharField()
    plan = MultipleChoiceGridField(required=False, widget=PlanningGridWidget())


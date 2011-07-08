#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from planning_grid.widgets import PlanningGridWidget

class MyTestForm(forms.Form):
    user = forms.CharField()
    plan = myforms.MultipleChoiceGridField(widget=PlanningGridWidget())


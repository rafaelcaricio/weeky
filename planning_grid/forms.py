#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class PlanningCellWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(PlanningCellWidget, self).__init__(*args, **kwargs)

class PlanningGridWidget(forms.MultiWidget):
    def __init__(self, attrs={}):
        # create the widgets
        super(PlanningGridWidget, self).__init__(widgets, attrs)

class MultipleChoiceGridField(forms.MultipleChoiceField):
    pass

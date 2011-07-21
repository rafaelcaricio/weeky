#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Weeky
# https://github.com/rafaelcaricio/weeky
#
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Rafael Caricio rafael@caricio.com

import calendar

from django.conf import settings
from django.utils.safestring import mark_safe
from django import forms

PERIODS_OF_DAY = getattr(settings, u'PERIODS_OF_DAY', (u'Morning', u'Midday', u'Evening'))

class PlanningCellWidget(forms.Textarea):
    def __init__(self, period_of_day, week_day, **kwargs):
        super(PlanningCellWidget, self).__init__(**kwargs)
        self.period_of_day = period_of_day
        self.week_day = week_day

    @property
    def cell_name(self):
        return u'%s_%s' % (self.week_day[:3], self.period_of_day)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(PlanningCellWidget, self).build_attrs(extra_attrs, **kwargs)

        attrs[u'id'] = u'%s_id' % self.cell_name.lower()

        if not u'name' in attrs:
            attrs[u'name'] = self.cell_name

        return attrs

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        attrs.update({"class": "hide"})

        textarea = super(PlanningCellWidget, self).render(name, value, attrs)

        return mark_safe(u'<div class="planningCell_container"><div class="tabHandler" tabindex="0"></div>\
                <div class="planningCell_display">%s</div>%s</div>' % (value or "", textarea))

class PlanningGridWidget(forms.MultiWidget):

    class Media:
        css = {
                "all": [
                    "css/planning_grid/PlanningGridWidget.css"
                ]
        }

        js = (
            "js/planning_grid/PlanningGridWidget.js",
        )

    def __init__(self, week_starts_in=calendar.MONDAY, attrs={}):
        self.planning_cells = []
        self.planning_calendar = calendar.Calendar(week_starts_in)

        for period_of_day in PERIODS_OF_DAY:
            for week_day in self.planning_calendar.iterweekdays():
                self.planning_cells.append(PlanningCellWidget(period_of_day, calendar.day_name[week_day], attrs=attrs))

        super(PlanningGridWidget, self).__init__(self.planning_cells, attrs)

    def format_output(self, rendered_widgets):
        sequence = 0
        planning_table = [u'<table class="planningGrid"><tr><th class="planningGrid_column_header"></th>']

        for week_day in self.planning_calendar.iterweekdays():
            planning_table.append(u'<th class="planningGrid_column_header">%s</th>' % calendar.day_name[week_day][:3])
        planning_table.append(u'</tr>')

        for period_of_day in PERIODS_OF_DAY:
            planning_table.append(u'<tr><th class="planningGrid_row_header">%s</th>' % period_of_day)
            for week_day in self.planning_calendar.iterweekdays():
                planning_table.append(u'<td class="planningGrid_data_cell">%s</td>' % rendered_widgets[sequence])
                sequence += 1
            planning_table.append(u'</tr>')

        planning_table.append(u'</table>')
        return mark_safe(u''.join(planning_table))

    def value_from_datadict(self, data, files, name):
        value = {}
        for i, widget in enumerate(self.widgets):
            value[widget.cell_name] = widget.value_from_datadict(data, files, name + '_%s' % i)
        return value

    def decompress(self, value):
        if value:
            return [widget.cell_name in value and value[widget.cell_name] or None for widget in self.widgets]
        else:
            return []

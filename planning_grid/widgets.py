#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        planning_table = [u'<table><tr><th></th>']

        for week_day in self.planning_calendar.iterweekdays():
            planning_table.append(u'<th>%s</th>' % calendar.day_name[week_day][:3])
        planning_table.append(u'</tr>')

        for period_of_day in PERIODS_OF_DAY:
            planning_table.append(u'<tr><th>%s</th>' % period_of_day)
            for week_day in self.planning_calendar.iterweekdays():
                planning_table.append(u'<td>%s</td>' % rendered_widgets[sequence])
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

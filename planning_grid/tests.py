#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from planning_grid.forms import PlanningCellWidget

class PlanningCellWidgetTest(TestCase):

    def test_setting_custom_attributes(self):
        cell = PlanningCellWidget(attrs={'id': 'my_custom_id'})
        self.assertTrue('id="my_custom_id"' in cell.render("casa", ""))

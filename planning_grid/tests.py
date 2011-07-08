#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree

from django.test import TestCase

from planning_grid.widgets import PlanningCellWidget, PlanningGridWidget

class PlanningCellWidgetTest(TestCase):

    def test_setting_custom_attributes(self):
        cell = PlanningCellWidget('Morning', 'Sunday', attrs={'bla': 'my_custom_attr'})
        element = ElementTree.fromstring(cell.render("casa", ""))
        self.assertEquals(element.get("bla"), "my_custom_attr")

    def test_create_attrs_relative_to_params(self):
        cell = PlanningCellWidget('Morning', 'Sunday', attrs={'bla': 'my_custom_attr'})
        attrs = cell.build_attrs()
        self.assertEqual(attrs['id'], 'sun_morning_id')
        self.assertEqual(attrs['name'], 'Sun_Morning')

    def test_use_field_name_when_passed_but_not_id(self):
        cell = PlanningCellWidget('Midday', 'Monday', attrs={
            "id": "not_used",
            "name": "use_this_name"
        })
        attrs = cell.build_attrs()
        self.assertEqual(attrs['id'], 'mon_midday_id')
        self.assertEqual(attrs['name'], 'use_this_name')

class PlanningGridWidgetTest(TestCase):

    def test_creation_of_widget(self):
        plan = PlanningGridWidget()
        self.assertTrue(plan)
        self.assertEquals(len(plan.planning_cells), 21, "The number of cells is not 21")

    def test_plan_rendering_output(self):
        plan = PlanningGridWidget()
        element = ElementTree.fromstring(plan.render("week_planning", []))
        #print plan.render("week_plan", [])

        self.assertEquals(element.tag, "table", "should be use a table to store the cells of planning")

        first_tr = element.find('tr')
        plan_week_days = first_tr.findall('th')[1:]

        self.assertEquals(len(plan_week_days), 7, "should be 7 week days")
        self.assertEquals(plan_week_days[0].text, "Mon", "the first day of week should be Mon")
        self.assertEquals(plan_week_days[-1].text, "Sun", "the last day of week should be Sun")

        periods_of_day = element.findall('tr')[1:]

        self.assertEquals(len(periods_of_day), 3, "should be 3 periods of day")
        self.assertEquals(periods_of_day[0].find('th').text, "Morning", "should be 'Morning'")
        self.assertEquals(periods_of_day[1].find('th').text, "Midday", "should be 'Midday'")
        self.assertEquals(periods_of_day[2].find('th').text, "Evening", "should be 'Evening'")

    def test_plan_from_data(self):
        plan = PlanningGridWidget()
        data_dict = {}
        for i in xrange(21):
            data_dict["week_plan_%d" % i] = i == 0 and "Gym" or str(i)

        value = plan.value_from_datadict(data_dict, None, "week_plan")

        self.assertEquals(type(value), dict, "should be a dict")
        self.assertTrue("Mon_Morning" in value, "should have the 'Mon_Morning' key in result value")
        self.assertEquals(value["Mon_Morning"], "Gym", "should have the 'Gym' at 'Mon_Morning'")
        self.assertEquals(len(value.keys()), 21, "should have 21 keys for activities")


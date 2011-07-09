#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree

from django.core.exceptions import ValidationError
from django.test import TestCase

from planning_grid.widgets import PlanningCellWidget, PlanningGridWidget
from planning_grid.fields import MultipleChoiceGridField

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
        for i in xrange(len(plan.planning_cells)):
            data_dict["week_plan_%d" % i] = i == 0 and "Gym" or str(i)

        value = plan.value_from_datadict(data_dict, None, "week_plan")

        self.assertEquals(type(value), dict, "should be a dict")
        self.assertTrue("Mon_Morning" in value, "should have the 'Mon_Morning' key in result value")
        self.assertEquals(value["Mon_Morning"], "Gym", "should have the 'Gym' at 'Mon_Morning'")
        self.assertEquals(len(value.keys()), 21, "should have 21 keys for activities")

    def test_decompress_value(self):
        plan = PlanningGridWidget()
        data_dict = {}
        for i in xrange(len(plan.planning_cells)):
            data_dict["week_plan_%d" % i] = i == 0 and "Gym" or str(i)

        value = plan.value_from_datadict(data_dict, None, "week_plan")

        decompressed_value = plan.decompress(value)

        self.assertEquals(type(decompressed_value), list, "should be a list of values")
        self.assertEquals(decompressed_value[0], "Gym", "the first value should be 'Gym'")
        self.assertEquals(decompressed_value[-1], "20", "the last value should be '20'")
        self.assertEquals(len(decompressed_value), 21, "should have 21 values")

    def test_decompress_value_with_empty_dict(self):
        plan = PlanningGridWidget()
        decompressed_value = plan.decompress({})
        self.assertEquals(decompressed_value, [], "should be a empty list")

    def test_decompress_value_with_partial_populated_dict(self):
        plan = PlanningGridWidget()
        data_dict = {}
        for i in xrange(len(plan.planning_cells) - 10):
            data_dict["week_plan_%d" % i] = i == 0 and "Gym" or str(i)

        value = plan.value_from_datadict(data_dict, None, "week_plan")

        decompressed_value = plan.decompress(value)

        self.assertEquals(type(decompressed_value), list, "should be a list of values")
        self.assertEquals(len(decompressed_value), 21, "should have 21 values")
        self.assertEquals(decompressed_value[-1], None, "the last value should be None")
 
class MultipleChoiceGridFieldTest(TestCase):

    def test_creation_of_field(self):
        field = MultipleChoiceGridField()
        self.assertTrue(field)
        self.assertEquals(type(field.widget), PlanningGridWidget, "the default widget should be PlanningGridWidget")
        self.assertTrue('invalid_dict' in field.default_error_messages, "should have a message for invalid dict")

    def test_to_python_of_a_valid_value(self):
        field = MultipleChoiceGridField()
        self.assertEquals(field.to_python({u"Mon_Midday": u"Gym"}), {u"Mon_Midday": u"Gym"}, "should return the same value")

    def test_to_python_of_a_none_value(self):
        field = MultipleChoiceGridField()
        self.assertEquals(field.to_python(None), {}, "should return a empty dict")

    def test_to_python_of_a_invalid_value(self):
        field = MultipleChoiceGridField()
        self.assertRaises(ValidationError, field.to_python, [u"Mon_Midday"])

    def test_validation_required_and_empty_value(self):
        field = MultipleChoiceGridField()
        self.assertRaises(ValidationError, field.validate, {})
        self.assertRaises(ValidationError, field.validate, {u'Mon_Midday': u''})

    def test_validation_not_required_and_empty_value(self):
        field = MultipleChoiceGridField(required=False)
        self.assertEquals(field.validate({}), None, "should execute without any exceptions")

    def test_validation_required_and_with_value(self):
        field = MultipleChoiceGridField()
        self.assertEquals(field.validate({u'Mon_Midday': u'Gym'}), None, "should execute without any exceptions")



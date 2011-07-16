#!/usr/bin/env python

from django.test import TestCase

class PlanningGridViewTest(TestCase):

    def test_access_form_page(self):
        response = self.client.get('/mytestview/')
        self.assertContains(response, '<table class="planningGrid">', status_code=200)

    def test_send_form_with_erros_the_correct_values_should_be_displayed_in_the_form_fiels(self):
        response = self.client.post('/mytestview/', {'plan_1': 'onlyonevalue'})
        self.assertContains(response, '>onlyonevalue</textarea>', status_code=200)


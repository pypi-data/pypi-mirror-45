# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class ProtectionPoliciesTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ProtectionPoliciesTests, cls).setUpClass()
        cls.controller = cls.api_client.protection_policies

    # Todo: Add description for test test_test_get_protection_policies
    def test_test_get_protection_policies(self):
        # Parameters for the API call
        all_under_hierarchy = None
        environments = None
        ids = None
        names = None
        tenant_ids = None
        vault_ids = None

        # Perform the API call through the SDK function
        result = self.controller.get_protection_policies(all_under_hierarchy, environments, ids, names, tenant_ids, vault_ids)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"id":"","name":"","incrementalSchedulingPolicy":{"periodicity":"kMonthly'
            '","monthlySchedule":{"day":"kSunday","dayCount":"kFirst"}},"retries":0,"ret'
            'ryIntervalMins":0,"daysToKeep":0}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



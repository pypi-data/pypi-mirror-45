# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class GroupsTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(GroupsTests, cls).setUpClass()
        cls.controller = cls.api_client.groups

    # Todo: Add description for test test_test_get_groups
    def test_test_get_groups(self):
        # Parameters for the API call
        all_under_hierarchy = None
        domain = None
        name = None
        tenant_ids = None

        # Perform the API call through the SDK function
        result = self.controller.get_groups(all_under_hierarchy, domain, name, tenant_ids)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"createdTimeMsecs":0,"description":"string","domain":"string","isSmbPrin'
            'cipalOnly":true,"lastUpdatedTimeMsecs":0,"name":"string","restricted":true,'
            '"roles":["string"],"sid":"string","smbPrincipals":[{"domain":"string","name'
            '":"string","sid":"string","type":"string"}]}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



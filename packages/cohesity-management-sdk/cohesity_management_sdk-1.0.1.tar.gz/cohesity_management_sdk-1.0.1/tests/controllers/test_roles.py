# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class RolesTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(RolesTests, cls).setUpClass()
        cls.controller = cls.api_client.roles

    # Todo: Add description for test test_test_get_roles
    def test_test_get_roles(self):
        # Parameters for the API call
        name = ''

        # Perform the API call through the SDK function
        result = self.controller.get_roles(name)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"name":"","label":"","privileges":[],"description":"","createdTimeMsecs"'
            ':0,"lastUpdatedTimeMsecs":0,"isCustomRole":false}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class TenantTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(TenantTests, cls).setUpClass()
        cls.controller = cls.api_client.tenant

    # Todo: Add description for test test_test_get_tenants
    def test_test_get_tenants(self):
        # Parameters for the API call
        hierarchy = None
        ids = None
        include_self = None
        properties = None
        status = None

        # Perform the API call through the SDK function
        result = self.controller.get_tenants(hierarchy, ids, include_self, properties, status)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('[]')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


    # Todo: Add description for test test_test_get_tenants_1
    def test_test_get_tenants_1(self):
        # Parameters for the API call
        hierarchy = None
        ids = None
        include_self = None
        properties = None
        status = None

        # Perform the API call through the SDK function
        result = self.controller.get_tenants(hierarchy, ids, include_self, properties, status)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('[]')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



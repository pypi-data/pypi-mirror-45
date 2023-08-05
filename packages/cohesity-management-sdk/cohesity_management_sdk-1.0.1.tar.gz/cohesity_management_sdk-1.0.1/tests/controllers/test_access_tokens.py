# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper
from cohesity_management_sdk.models.access_token_credential_model import AccessTokenCredentialModel


class AccessTokensTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(AccessTokensTests, cls).setUpClass()
        cls.controller = cls.api_client.access_tokens

    # Todo: Add description for test test_test_generate_access_token
    def test_test_generate_access_token(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"username":"admin","password":"admin"}', AccessTokenCredentialModel.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.create_generate_access_token(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"accessToken":"string","privileges":["string"],"tokenType":"string"}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


    # Todo: Add description for test test_test_generate_access_token_1
    def test_test_generate_access_token_1(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{\'username\':\'admin\',\'password\':\'admin\'}', AccessTokenCredentialModel.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.create_generate_access_token(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"accessToken":"","tokenType":"","privileges":[]}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



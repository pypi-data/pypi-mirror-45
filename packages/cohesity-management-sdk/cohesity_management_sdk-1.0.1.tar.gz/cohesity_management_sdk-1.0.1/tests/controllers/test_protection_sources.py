# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class ProtectionSourcesTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ProtectionSourcesTests, cls).setUpClass()
        cls.controller = cls.api_client.protection_sources

    # Todo: Add description for test test_test_list_virtual_machines
    def test_test_list_virtual_machines(self):
        # Parameters for the API call
        names = None
        protected = None
        uuids = None
        v_center_id = None

        # Perform the API call through the SDK function
        result = self.controller.list_virtual_machines(names, protected, uuids, v_center_id)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"id":0,"parentId":0,"name":"","environment":"kVMware","vmWareProtectionS'
            'ource":{"type":"kVirtualMachine","name":"","id":{"uuid":"","morItem":"","mo'
            'rType":""},"connectionState":"kConnected","toolsRunningStatus":"kGuestTools'
            'Running","hasPersistentAgent":true,"virtualDisks":[{"filename":"","controll'
            'erType":"SCSI","busNumber":0,"unitNumber":0}]}}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class VaultsTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(VaultsTests, cls).setUpClass()
        cls.controller = cls.api_client.vaults

    # Todo: Add description for test test_test_get_vaults
    def test_test_get_vaults(self):
        # Parameters for the API call
        id = None
        include_marked_for_removal = None
        name = None

        # Perform the API call through the SDK function
        result = self.controller.get_vaults(id, include_marked_for_removal, name)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)


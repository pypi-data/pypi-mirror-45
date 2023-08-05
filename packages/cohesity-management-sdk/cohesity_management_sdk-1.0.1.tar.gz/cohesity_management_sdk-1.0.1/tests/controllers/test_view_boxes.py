# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class ViewBoxesTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ViewBoxesTests, cls).setUpClass()
        cls.controller = cls.api_client.view_boxes

    # Todo: Add description for test test_test_get_view_boxes
    def test_test_get_view_boxes(self):
        # Parameters for the API call
        all_under_hierarchy = None
        cluster_partition_ids = None
        fetch_stats = None
        ids = None
        names = None
        tenant_ids = None

        # Perform the API call through the SDK function
        result = self.controller.get_view_boxes(all_under_hierarchy, cluster_partition_ids, fetch_stats, ids, names, tenant_ids)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('[]')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class RemoteClusterTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(RemoteClusterTests, cls).setUpClass()
        cls.controller = cls.api_client.remote_cluster

    # Todo: Add description for test test_test_get_remote_clusters
    def test_test_get_remote_clusters(self):
        # Parameters for the API call
        cluster_ids = None
        cluster_names = None
        purpose_remote_access = None
        purpose_replication = None

        # Perform the API call through the SDK function
        result = self.controller.get_remote_clusters(cluster_ids, cluster_names, purpose_remote_access, purpose_replication)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('[]')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



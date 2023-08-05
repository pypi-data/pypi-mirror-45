# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class ClusterPartitionsTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ClusterPartitionsTests, cls).setUpClass()
        cls.controller = cls.api_client.cluster_partitions

    # Todo: Add description for test test_test_get_cluster_partition
    def test_test_get_cluster_partition(self):
        # Parameters for the API call
        ids = APIHelper.json_deserialize('')
        names = None

        # Perform the API call through the SDK function
        result = self.controller.get_cluster_partitions(ids, names)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"hostName":"string","id":0,"name":"string","nodeIds":[0],"vips":["string'
            '"],"vlanIps":["string"],"vlans":[{"addToClusterPartition":true,"description'
            '":"string","gateway":"string","hostname":"string","id":0,"interfaceName":"s'
            'tring","ips":["string"],"subnet":{"description":"string","ip":"string","net'
            'maskBits":0,"netmaskIp4":"string"},"tenantId":"string","vlanName":"string"}'
            ']}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



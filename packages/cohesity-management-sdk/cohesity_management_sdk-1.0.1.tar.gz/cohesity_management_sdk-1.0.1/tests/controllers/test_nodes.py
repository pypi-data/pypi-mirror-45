# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class NodesTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(NodesTests, cls).setUpClass()
        cls.controller = cls.api_client.nodes

    # Todo: Add description for test test_test_get_nodes
    def test_test_get_nodes(self):

        # Perform the API call through the SDK function
        result = self.controller.get_nodes()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"capacityByTier":[],"chassisInfo":{},"clusterPartitionId":0,"clusterPart'
            'itionName":"string","diskCount":0,"id":0,"ip":"string","isMarkedForRemoval"'
            ':true,"maxPhysicalCapacityBytes":0,"nodeHardwareInfo":{},"nodeIncarnationId'
            '":0,"nodeSoftwareVersion":"string","offlineMountPathsOfDisks":[],"removalRe'
            'ason":[],"removalState":"kDontRemove","stats":{},"systemDisks":[]}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class ProtectionJobsTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ProtectionJobsTests, cls).setUpClass()
        cls.controller = cls.api_client.protection_jobs

    # Todo: Add description for test test_test_get_protection_jobs
    def test_test_get_protection_jobs(self):
        # Parameters for the API call
        all_under_hierarchy = None
        environments = None
        ids = None
        include_last_run_and_stats = None
        is_active = None
        is_deleted = None
        names = None
        only_return_basic_summary = None
        policy_ids = None
        tenant_ids = None

        # Perform the API call through the SDK function
        result = self.controller.get_protection_jobs(all_under_hierarchy, environments, ids, include_last_run_and_stats, is_active, is_deleted, names, only_return_basic_summary, policy_ids, tenant_ids)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"id":1576,"name":"automation_job","environment":"kVMware","policyId":"61'
            '23432859864663:1547505014317:1373","viewBoxId":5,"parentSourceId":3,"source'
            'Ids":[],"startTime":{},"timezone":"America/Los_Angeles","incrementalProtect'
            'ionSlaTimeMins":60,"fullProtectionSlaTimeMins":120,"priority":"kMedium","al'
            'ertingPolicy":[],"indexingPolicy":{"disableIndexing":false,"allowPrefixes":'
            '[],"denyPrefixes":[]},"qosType":"kBackupHDD","environmentParameters":{"vmwa'
            'reParameters":{"fallbackToCrashConsistent":true}},"uid":{"id":0,"clusterId"'
            ':0,"clusterIncarnationId":0},"policyAppliedTimeMsecs":0,"modificationTimeUs'
            'ecs":0,"modifiedByUser":"","creationTimeUsecs":0}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



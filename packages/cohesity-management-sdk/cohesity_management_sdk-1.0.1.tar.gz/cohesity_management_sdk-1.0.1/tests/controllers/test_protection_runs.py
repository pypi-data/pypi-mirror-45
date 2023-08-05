# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class ProtectionRunsTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ProtectionRunsTests, cls).setUpClass()
        cls.controller = cls.api_client.protection_runs

    # Todo: Add description for test test_test_get_protection_runs
    def test_test_get_protection_runs(self):
        # Parameters for the API call
        end_time_usecs = None
        exclude_error_runs = None
        exclude_non_restoreable_runs = None
        exclude_tasks = None
        job_id = None
        num_runs = None
        run_types = None
        source_id = None
        start_time_usecs = None
        started_time_usecs = None

        # Perform the API call through the SDK function
        result = self.controller.get_protection_runs(end_time_usecs, exclude_error_runs, exclude_non_restoreable_runs, exclude_tasks, job_id, num_runs, run_types, source_id, start_time_usecs, started_time_usecs)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)

    # Todo: Add description for test test_test_get_protection_runs_1
    def test_test_get_protection_runs_1(self):
        # Parameters for the API call
        end_time_usecs = None
        exclude_error_runs = None
        exclude_non_restoreable_runs = None
        exclude_tasks = None
        job_id = None
        num_runs = None
        run_types = None
        source_id = None
        start_time_usecs = None
        started_time_usecs = None

        # Perform the API call through the SDK function
        result = self.controller.get_protection_runs(end_time_usecs, exclude_error_runs, exclude_non_restoreable_runs, exclude_tasks, job_id, num_runs, run_types, source_id, start_time_usecs, started_time_usecs)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('[]')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



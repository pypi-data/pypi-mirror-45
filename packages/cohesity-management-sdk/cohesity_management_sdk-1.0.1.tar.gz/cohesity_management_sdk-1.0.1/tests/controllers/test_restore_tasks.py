# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class RestoreTasksTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(RestoreTasksTests, cls).setUpClass()
        cls.controller = cls.api_client.restore_tasks

    # Todo: Add description for test test_test_get_restore_tasks
    def test_test_get_restore_tasks(self):
        # Parameters for the API call
        end_time_usecs = None
        environment = None
        page_count = None
        start_time_usecs = None
        task_ids = None
        task_types = None

        # Perform the API call through the SDK function
        result = self.controller.get_restore_tasks(end_time_usecs, environment, page_count, start_time_usecs, task_ids, task_types)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"id":0,"type":"kCloneView","status":"kFinished","username":"","startTime'
            'Usecs":0,"endTimeUsecs":0,"fullViewName":"","targetViewCreated":true,"name"'
            ':"","objects":[{}],"continueOnError":true,"cloneViewParameters":{"descripti'
            'on":"","storagePolicyOverride":{"disableInlineDedupAndCompression":false},"'
            'qos":{"principalName":""}}}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



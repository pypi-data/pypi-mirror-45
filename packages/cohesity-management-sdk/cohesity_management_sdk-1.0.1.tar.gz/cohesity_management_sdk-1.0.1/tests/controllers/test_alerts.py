# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class AlertsTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(AlertsTests, cls).setUpClass()
        cls.controller = cls.api_client.alerts

    # Todo: Add description for test test_test_get_alerts
    def test_test_get_alerts(self):
        # Parameters for the API call
        max_alerts = 1
        alert_category_list = None
        alert_id_list = None
        alert_severity_list = None
        alert_state_list = None
        alert_type_list = None
        all_under_hierarchy = None
        end_date_usecs = None
        property_key = None
        property_value = None
        resolution_id_list = None
        start_date_usecs = None
        tenant_ids = None

        # Perform the API call through the SDK function
        result = self.controller.get_alerts(max_alerts, alert_category_list, alert_id_list, alert_severity_list, alert_state_list, alert_type_list, all_under_hierarchy, end_date_usecs, property_key, property_value, resolution_id_list, start_date_usecs, tenant_ids)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"id":"","alertCode":"","firstTimestampUsecs":0,"latestTimestampUsecs":0,'
            '"alertCategory":"kCluster","alertType":0,"severity":"kInfo","alertState":"k'
            'Open","propertyList":[],"dedupTimestamps":[0],"dedupCount":1,"alertDocument'
            '":{"alertName":"","alertDescription":"","alertCause":"","alertHelpText":""}'
            '}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



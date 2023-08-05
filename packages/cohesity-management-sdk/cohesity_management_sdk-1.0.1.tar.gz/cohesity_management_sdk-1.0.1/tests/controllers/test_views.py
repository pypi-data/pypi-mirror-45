# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class ViewsTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ViewsTests, cls).setUpClass()
        cls.controller = cls.api_client.views

    # Todo: Add description for test test_test_get_views
    def test_test_get_views(self):
        # Parameters for the API call
        sort_by_logical_usage = None
        all_under_hierarchy = None
        include_inactive = None
        job_ids = None
        match_alias_names = None
        match_partial_names = None
        max_count = None
        max_view_id = None
        tenant_ids = None
        view_box_ids = None
        view_box_names = None
        view_names = None

        # Perform the API call through the SDK function
        result = self.controller.get_views(sort_by_logical_usage, all_under_hierarchy, include_inactive, job_ids, match_alias_names, match_partial_names, max_count, max_view_id, tenant_ids, view_box_ids, view_box_names, view_names)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"views":[{"name":"","viewId":0,"viewBoxId":0,"viewBoxName":"","createTime'
            'Msecs":0,"basicMountPath":"","nfsMountPath":"","caseInsensitiveNamesEnabled'
            '":false,"logicalUsageBytes":0,"description":"","storagePolicyOverride":{"di'
            'sableInlineDedupAndCompression":true},"allowMountOnWindows":false,"protocol'
            'Access":"kNFSOnly","enableMinion":true,"enableFilerAuditLogging":false,"ena'
            'bleMixedModePermissions":false,"securityMode":"kNativeMode","enableSmbAcces'
            'sBasedEnumeration":false,"enableSmbViewDiscovery":false,"enableNfsViewDisco'
            'very":false}],"lastResult":true,"count":0}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


    # Todo: Add description for test test_test_get_views_1
    def test_test_get_views_1(self):
        # Parameters for the API call
        sort_by_logical_usage = None
        all_under_hierarchy = None
        include_inactive = None
        job_ids = None
        match_alias_names = None
        match_partial_names = None
        max_count = None
        max_view_id = None
        tenant_ids = None
        view_box_ids = None
        view_box_names = None
        view_names = None

        # Perform the API call through the SDK function
        result = self.controller.get_views(sort_by_logical_usage, all_under_hierarchy, include_inactive, job_ids, match_alias_names, match_partial_names, max_count, max_view_id, tenant_ids, view_box_ids, view_box_names, view_names)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"views":[],"lastResult":true,"count":20}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



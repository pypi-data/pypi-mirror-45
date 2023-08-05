# -*- coding: utf-8 -*-

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from cohesity_management_sdk.api_helper import APIHelper


class ClusterTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ClusterTests, cls).setUpClass()
        cls.controller = cls.api_client.cluster

    # Todo: Add description for test test_test_get_cluster
    def test_test_get_cluster(self):
        # Parameters for the API call
        fetch_stats = None

        # Perform the API call through the SDK function
        result = self.controller.get_cluster(fetch_stats)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"availableMetadataSpace":0,"bondingMode":"ActiveBackup","clusterAuditLogC'
            'onfig":{"enabled":true,"retentionPeriodDays":0},"clusterSoftwareVersion":"s'
            'tring","clusterType":"kPhysical","createdTimeMsecs":0,"currentOpScheduledTi'
            'meSecs":0,"currentOperation":"kRemoveNode","currentTimeMsecs":0,"dnsServerI'
            'ps":["string"],"domainNames":["string"],"enableActiveMonitoring":true,"enab'
            'leUpgradePkgPolling":true,"encryptionEnabled":true,"encryptionKeyRotationPe'
            'riodSecs":0,"eulaConfig":{"licenseKey":"string","signedByUser":"string","si'
            'gnedTime":0,"signedVersion":0},"filerAuditLogConfig":{"enabled":true,"reten'
            'tionPeriodDays":0},"fipsModeEnabled":true,"gateway":"string","hardwareInfo"'
            ':{"hardwareModels":["string"],"hardwareVendors":["string"]},"id":0,"incarna'
            'tionId":0,"isDocumentationLocal":true,"languageLocale":"string","metadataFa'
            'ultToleranceFactor":0,"mtu":0,"multiTenancyEnabled":true,"name":"string","n'
            'odeCount":0,"ntpSettings":{"ntpServersInternal":true},"reverseTunnelEnabled'
            '":true,"reverseTunnelEndTimeMsecs":0,"smbAdDisabled":true,"stats":{"cloudUs'
            'agePerfStats":{"dataInBytes":0,"dataInBytesAfterReduction":0,"minUsablePhys'
            'icalCapacityBytes":0,"numBytesRead":0,"numBytesWritten":0,"physicalCapacity'
            'Bytes":0,"readIos":0,"readLatencyMsecs":0,"systemCapacityBytes":0,"systemUs'
            'ageBytes":0,"totalPhysicalRawUsageBytes":0,"totalPhysicalUsageBytes":0,"wri'
            'teIos":0,"writeLatencyMsecs":0},"dataReductionRatio":0,"id":0,"localUsagePe'
            'rfStats":{"dataInBytes":0,"dataInBytesAfterReduction":0,"minUsablePhysicalC'
            'apacityBytes":0,"numBytesRead":0,"numBytesWritten":0,"physicalCapacityBytes'
            '":0,"readIos":0,"readLatencyMsecs":0,"systemCapacityBytes":0,"systemUsageBy'
            'tes":0,"totalPhysicalRawUsageBytes":0,"totalPhysicalUsageBytes":0,"writeIos'
            '":0,"writeLatencyMsecs":0},"logicalStats":{"totalLogicalUsageBytes":0},"usa'
            'gePerfStats":{"dataInBytes":0,"dataInBytesAfterReduction":0,"minUsablePhysi'
            'calCapacityBytes":0,"numBytesRead":0,"numBytesWritten":0,"physicalCapacityB'
            'ytes":0,"readIos":0,"readLatencyMsecs":0,"systemCapacityBytes":0,"systemUsa'
            'geBytes":0,"totalPhysicalRawUsageBytes":0,"totalPhysicalUsageBytes":0,"writ'
            'eIos":0,"writeLatencyMsecs":0}},"supportedConfig":{"minNodesAllowed":0,"sup'
            'portedErasureCoding":["string"]},"syslogServers":[{"address":"string","isCl'
            'usterAuditingEnabled":true,"isFilerAuditingEnabled":true,"name":"string","p'
            'ort":0,"protocol":"kUDP"}],"targetSoftwareVersion":"string","tenantViewboxS'
            'haringEnabled":true,"timezone":"string","turboMode":true,"usedMetadataSpace'
            'Pct":0}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


    # Todo: Add description for test test_test_get_basic_cluster_info
    def test_test_get_basic_cluster_info(self):

        # Perform the API call through the SDK function
        result = self.controller.get_basic_cluster_info()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"name":"","clusterType":"kPhysical","languageLocale":" ","clusterSoftware'
            'Version":"","authenticationType":0,"domains":[""],"mcmMode":false,"idpConfi'
            'gured":false,"idpTenantExists":false}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))



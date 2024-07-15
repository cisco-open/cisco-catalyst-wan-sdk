# Copyright 2024 Cisco Systems, Inc. and its affiliates

from catalystwan.integration_tests.base import TestCaseBase
from catalystwan.utils.config_migration.runner import ConfigMigrationRunner
from catalystwan.workflows.config_migration import DEVICE_TYPE_BLOCKLIST


class TestMigrationFlow(TestCaseBase):
    runner: ConfigMigrationRunner

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.runner = ConfigMigrationRunner.collect_push_and_rollback(cls.session)
        cls.runner.run()

    def test_collect_artefact(self):
        # Arrange
        collect_result = self.runner.load_collect_result()
        # Act, Assert
        for item in collect_result.excluded_items:
            assert item.element_type in DEVICE_TYPE_BLOCKLIST

    def test_transform_artefact(self):
        # Arrange
        transform_result = self.runner.load_transform_result()
        # Act, Assert
        assert transform_result.failed_items == list()

    def test_push_artefact(self):
        # Arrange
        push_result = self.runner.load_push_result()
        # Act, Assert
        assert push_result.report.failed_push_parcels == list()

    def test_rollback_artefact(self):
        # Arrange
        rollback_result = self.runner.load_rollback_result()
        # Act, Assert
        assert rollback_result.failed_items == list()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.runner.clear_ux2()
        super().tearDownClass()

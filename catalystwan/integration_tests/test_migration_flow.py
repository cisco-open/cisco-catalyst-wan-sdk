# Copyright 2024 Cisco Systems, Inc. and its affiliates

import unittest

from catalystwan.integration_tests.base import TestCaseBase
from catalystwan.utils.config_migration.runner import ConfigMigrationRunner


class TestMigrationFlow(TestCaseBase):
    runner: ConfigMigrationRunner

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.runner = ConfigMigrationRunner.collect_push_and_rollback(cls.session)
        cls.runner.dump_schemas()
        # cls.runner.run()

    @unittest.skip("Testing purpose only")
    def test_collect_artefact(self):
        # Arrange
        ux1_config = self.runner.load_collected_config()
        # Act, Assert
        assert ux1_config

    @unittest.skip("Testing purpose only")
    def test_transform_artefact(self):
        # Arrange
        transform_result = self.runner.load_transform_result()
        # Act, Assert
        assert transform_result.failed_items == list()

    @unittest.skip("Testing purpose only")
    def test_push_artefact(self):
        # Arrange
        push_result = self.runner.load_push_result()
        # Act, Assert
        assert push_result.report.failed_push_parcels == list()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.runner.clear_ux2()
        super().tearDownClass()

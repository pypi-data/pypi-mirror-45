# -*- coding: utf-8 -*-
"""Test export file migration from export version 0.1 to 0.2"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os

from aiida.backends.testbase import AiidaTestCase
from aiida.cmdline.utils.migration.utils import verify_metadata_version
from aiida.cmdline.utils.migration.v01_to_v02 import migrate_v1_to_v2

from ..utils import get_json_files


class TestMigrateV01toV02(AiidaTestCase):
    """Test migration of export files from export version 0.1 to 0.2"""

    def test_migrate_v1_to_v2(self):
        """Test function migrate_v1_to_v2"""

        # Get metadata.json and data.json as dicts from v0.1 file fixture
        metadata_v1, data_v1 = get_json_files(
            "export_v0.1_no_UPF.aiida", core_file=True)
        verify_metadata_version(metadata_v1, version='0.1')

        # Get metadata.json and data.json as dicts from v0.2 file fixture
        metadata_v2, data_v2 = get_json_files(
            "export_v0.2_no_UPF.aiida", core_file=True)
        verify_metadata_version(metadata_v2, version='0.2')

        # Migrate to v0.2
        migrate_v1_to_v2(metadata_v1, data_v1)
        verify_metadata_version(metadata_v1, version='0.2')

        # Remove AiiDA version, since this may change irregardless of the migration function
        metadata_v1.pop('aiida_version')
        metadata_v2.pop('aiida_version')

        # Assert changes were performed correctly
        self.maxDiff = None  # pylint: disable=invalid-name
        self.assertDictEqual(
            metadata_v1,
            metadata_v2,
            msg=
            "After migration, metadata.json should equal intended metadata.json from fixture"
        )
        self.assertDictEqual(
            data_v1,
            data_v2,
            msg=
            "After migration, data.json should equal intended data.json from fixture"
        )

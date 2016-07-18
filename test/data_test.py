import unittest, os
from util import data_config as dc


class TestDataPaths(unittest.TestCase):
    """Test data access in the filesystem."""

    def setUp(self):
        """Sets up the test"""
        print("TestDataCRUD:setUp__:begin")
        self.data_config = dc
        self.db_targets = dc.DB_TARGETS()
        print("TestDataCRUD:setUp__:end")

    def tearDown(self):
        """Cleans up the test"""
        print("TestDataCRUD:tearDown__:begin")
        self.data_config = None
        self.db_targets = None
        print("TestDataCRUD:tearDown__:end")

    def test_character_dir(self):
        """verify a directory exists for character storage"""
        char_dir = dc.character_dir
        self.assertTrue(os.path.exists(char_dir),
            "{} does not exist.".format(char_dir))

    def test_mission_dir(self):
        """Verify directory exists for mission data"""
        mission_dir = self.db_targets.mission_data_dir
        self.assertTrue(os.path.exists(mission_dir),
            "{} does not exist.".format(mission_dir))

    def test_service_branch_dir(self):
        """Verify directory exists for service branch data"""
        service_dir = self.db_targets.service_branches
        self.assertTrue(os.path.exists(service_dir),
            "{} does not exist.".format(service_dir))



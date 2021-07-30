import unittest
from constants import Constants
from logger import Logger
from db_connection_pool import DBConnectionPool
from config import Config
from ratestask_helper import RatestaskHelper as rsh

class TestRatestaskMethods(unittest.TestCase):
    config = logger = db_conn_pool = None

    def setUp(self):
        if not TestRatestaskMethods.config:
            TestRatestaskMethods.config = Config()
            __builtins__.config = TestRatestaskMethods.config
        if not TestRatestaskMethods.logger:
            TestRatestaskMethods.logger = Logger()
            __builtins__.logger = TestRatestaskMethods.logger
        if not TestRatestaskMethods.db_conn_pool:
            TestRatestaskMethods.db_conn_pool = DBConnectionPool()
            __builtins__.db_conn_pool = TestRatestaskMethods.db_conn_pool


    def test_validate_string_1(self):
        date_from = '2016-01-01'
        self.assertTrue(rsh.validate_date(date_from))


    def test_validate_string_2(self):
        date_from = '01-01-2016'
        self.assertFalse(rsh.validate_date(date_from))


    def test_port_code(self):
        port_code = 'CNSGH'
        self.assertTrue(rsh.is_port_code(port_code=port_code))


    def test_region_slug(self):
        region_slug = 'baltic'
        self.assertTrue(rsh.is_region_slug(region_slug=region_slug))


    def test_child_region(self):
        region_slug = 'baltic'
        child_regions = rsh.get_child_region_for_region(region=region_slug)
        expected_child_regions = ['finland_main', 'baltic_main', 'poland_main', 'baltic']
        success = True
        if len(expected_child_regions) == len(child_regions):
            for child_region in child_regions:
                if child_region not in expected_child_regions:
                    success = False
                    break
        else:
            success = False
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
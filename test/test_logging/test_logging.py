import unittest
import src.utilities.logging as log

class TestLogging(unittest.TestCase):
    """
    Test class for Snippet related CRUD Services
    """

    def setUp(self):
        pass

    def test_log_level_name_success(self):
        self.assertEqual(log.get_level_name(2), 'Level 2')

if __name__=="__main__":
    unittest.main()
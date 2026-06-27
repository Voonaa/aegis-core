import sys
import unittest
from unittest.mock import MagicMock, patch
from packages.core.services.privilege_service import PrivilegeService

class TestPrivilegeService(unittest.TestCase):
    def setUp(self):
        self.service = PrivilegeService()

    def test_is_admin_check(self):
        # Simply check it returns a boolean value without crashing
        res = self.service.is_admin()
        self.assertIsInstance(res, bool)

    @patch("ctypes.windll", create=True)
    def test_is_admin_mocked_true(self, mock_windll):
        # Mock shell32.IsUserAnAdmin to return 1 (True)
        mock_windll.shell32.IsUserAnAdmin = MagicMock(return_value=1)
        self.assertTrue(self.service.is_admin())

    @patch("ctypes.windll", create=True)
    def test_is_admin_mocked_false(self, mock_windll):
        # Mock shell32.IsUserAnAdmin to return 0 (False)
        mock_windll.shell32.IsUserAnAdmin = MagicMock(return_value=0)
        self.assertFalse(self.service.is_admin())

    @patch("ctypes.windll", create=True)
    def test_is_admin_exception(self, mock_windll):
        # Simulate check exception
        mock_windll.shell32.IsUserAnAdmin.side_effect = Exception("Windll fail")
        self.assertFalse(self.service.is_admin())

    @patch("ctypes.windll", create=True)
    def test_relaunch_as_admin_already_admin(self, mock_windll):
        # If already admin, relaunch returns True instantly
        mock_windll.shell32.IsUserAnAdmin = MagicMock(return_value=1)
        self.assertTrue(self.service.relaunch_as_admin())

    @patch("ctypes.windll", create=True)
    @patch("sys.exit")
    def test_relaunch_as_admin_elevation_success(self, mock_exit, mock_windll):
        # If not admin, simulate ShellExecuteW success (> 32 return code)
        mock_windll.shell32.IsUserAnAdmin = MagicMock(return_value=0)
        mock_windll.shell32.ShellExecuteW = MagicMock(return_value=42)
        
        res = self.service.relaunch_as_admin()
        # sys.exit(0) should be triggered on success
        mock_exit.assert_called_once_with(0)

    @patch("ctypes.windll", create=True)
    def test_relaunch_as_admin_elevation_rejected(self, mock_windll):
        # Simulate elevation rejection (<= 32 error code)
        mock_windll.shell32.IsUserAnAdmin = MagicMock(return_value=0)
        mock_windll.shell32.ShellExecuteW = MagicMock(return_value=5)
        
        self.assertFalse(self.service.relaunch_as_admin())

if __name__ == "__main__":
    unittest.main()

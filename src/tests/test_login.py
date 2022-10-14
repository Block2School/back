import unittest
from services.login import LoginService
from unittest.mock import Mock, patch
from database import Database

class TestLogin(unittest.TestCase):
  # is_banned()
  @patch('services.login.LoginService.is_banned')
  def test_is_banned_true(self, mock_db):
    print(mock_db)
    print(dir(mock_db))
    mock_db.return_value = None
    uuid = mock_db.return_value
    print(uuid)
    # ban = LoginService.is_banned(uuid)
    # self.assertEqual(ban, None)
    # /admin/user

    # si requet ok -> data list d'object et y'a l'uuid 
    #



  def test_is_banned_empty_param(self):
    result = LoginService.is_banned('')
    self.assertEqual(result, None)



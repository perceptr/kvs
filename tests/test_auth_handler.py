import hashlib
import unittest
from unittest.mock import patch, MagicMock

import auth_handler
from auth_handler import AuthHandler


class FakeDBHandler:
    def __init__(self):
        self.execute_query_with_return = MagicMock()
        self.execute_query_with_no_return = MagicMock()


class TestAuthHandler(unittest.TestCase):
    def test_init(self):
        auth_handler.DBHandler = FakeDBHandler
        ah = AuthHandler(
            'database',
            'storage_name',
            'password',
        )
        self.assertEqual(ah._AuthHandler__database, 'database')
        self.assertEqual(ah._AuthHandler__storage_name, 'storage_name')
        self.assertEqual(ah._AuthHandler__hashed_password,
                         hashlib.sha256('password'.encode()).hexdigest())

    def test_check_if_login_exists(self):
        auth_handler.DBHandler = FakeDBHandler
        fake_db_handler = FakeDBHandler()
        ah = AuthHandler(
            fake_db_handler,
            'storage_name',
            'password',
        )
        actual = ah._AuthHandler__check_if_login_exists()
        fake_db_handler.execute_query_with_return.assert_called_once_with(
            "SELECT * FROM auth_table WHERE storage_name = 'storage_name'"
        )
        self.assertFalse(actual)

    def test_check_if_password_is_true(self):
        auth_handler.DBHandler = FakeDBHandler
        fake_db_handler = FakeDBHandler()
        ah = AuthHandler(
            fake_db_handler,
            'storage_name',
            'password',
        )
        actual = ah.check_if_password_is_true()
        fake_db_handler.execute_query_with_return.assert_called_once_with(
            "SELECT password FROM auth_table WHERE storage_name = "
            "'storage_name' AND password = '%s'" %
            ah._AuthHandler__hashed_password
        )
        self.assertFalse(actual)

    def test_add_to_auth_table(self):
        auth_handler.DBHandler = FakeDBHandler
        fake_db_handler = FakeDBHandler()
        ah = AuthHandler(
            fake_db_handler,
            'storage_name',
            'password',
        )
        ah._AuthHandler__add_to_auth_table()
        fake_db_handler.execute_query_with_no_return.assert_called_once_with(
            "INSERT INTO auth_table (storage_name, password) VALUES "
            "('storage_name', '%s')" % ah._AuthHandler__hashed_password
        )

    def test_authenticate(self):
        auth_handler.DBHandler = FakeDBHandler
        fake_db_handler = FakeDBHandler()
        ah = AuthHandler(
            fake_db_handler,
            'storage_name',
            'password',
        )
        ah._AuthHandler__check_if_login_exists = MagicMock(return_value=True)
        ah.check_if_password_is_true = MagicMock(return_value=False)
        ah._AuthHandler__add_to_auth_table = MagicMock()
        with self.assertRaises(Exception):
            ah.authenticate()

        ah._AuthHandler__check_if_login_exists.assert_called_once_with()
        ah.check_if_password_is_true.assert_called_once_with()

        ah._AuthHandler__check_if_login_exists = MagicMock(return_value=False)
        ah.authenticate()
        ah._AuthHandler__check_if_login_exists.assert_called_once_with()
        ah._AuthHandler__add_to_auth_table.assert_called_once_with()

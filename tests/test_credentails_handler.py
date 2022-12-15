import unittest
from unittest.mock import patch, MagicMock

import credentials_handler
from credentials_handler import CredentialsHandler


class FakeCursor:
    def __init__(self):
        self.execute = MagicMock()
        self.fetchone = MagicMock()


class TestCredentialsHandler(unittest.TestCase):
    def test_init(self):
        credentials_handler.sqlite3 = fake_sqlite3 = MagicMock()
        fake_cursor = FakeCursor()
        fake_sqlite3.connect.return_value = fake_sqlite3
        fake_sqlite3.cursor.return_value = fake_cursor
        ch = CredentialsHandler()
        self.assertEqual(ch._CredentialsHandler__cursor, fake_cursor)
        self.assertEqual(ch._CredentialsHandler__conn, fake_sqlite3)

        fake_cursor.execute.assert_called_once_with(
            """CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cred_name TEXT NOT NULL,
            cred_value TEXT NOT NULL
        )""")
        fake_sqlite3.commit.assert_called_once()

    @patch('credentials_handler.sqlite3', MagicMock())
    def test_insert_cred(self):
        fake_cursor = FakeCursor()
        credentials_handler.sqlite3.connect.return_value = \
            credentials_handler.sqlite3
        credentials_handler.sqlite3.cursor.return_value = fake_cursor
        ch = CredentialsHandler()
        ch.insert_cred('cred_name', 'cred_value')
        fake_cursor.execute.assert_called_with(
            "INSERT INTO credentials (cred_name, cred_value) VALUES (?, ?)",
            ('cred_name', 'cred_value'))
        credentials_handler.sqlite3.commit.assert_called()

    @patch('credentials_handler.sqlite3', MagicMock())
    def test_get_cred_by_name(self):
        fake_cursor = FakeCursor()
        credentials_handler.sqlite3.connect.return_value = \
            credentials_handler.sqlite3
        credentials_handler.sqlite3.cursor.return_value = fake_cursor
        ch = CredentialsHandler()
        ch.get_cred_by_name('cred_name')
        fake_cursor.execute.assert_called_with(
            "SELECT cred_value FROM credentials WHERE cred_name = ?",
            ('cred_name',))
        fake_cursor.fetchone.assert_called()

    @patch('credentials_handler.sqlite3', MagicMock())
    def test_delete_cred_by_name(self):
        fake_cursor = FakeCursor()
        credentials_handler.sqlite3.connect.return_value = \
            credentials_handler.sqlite3
        credentials_handler.sqlite3.cursor.return_value = fake_cursor
        ch = CredentialsHandler()
        ch._CredentialsHandler__delete_cred_by_name('cred_name')
        fake_cursor.execute.assert_called_with(
            "DELETE FROM credentials WHERE cred_name = ?",
            ('cred_name',))
        credentials_handler.sqlite3.commit.assert_called()






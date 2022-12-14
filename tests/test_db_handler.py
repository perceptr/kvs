import unittest
from unittest.mock import patch, MagicMock

import db_handler
from db_handler import DBHandler


class TestDBHandler(unittest.TestCase):
    @patch('db_handler.psycopg2', MagicMock())
    @patch('db_handler.logging', MagicMock())
    def test_init(self):
        db_handler.psycopg2 = fake_psycopg2 = MagicMock()
        fake_psycopg2.connect.return_value = fake_psycopg2
        fake_psycopg2.cursor.return_value = fake_psycopg2
        dbh = DBHandler(
            'user',
            'password',
            'host',
            'port',
            'database',
        )
        fake_psycopg2.cursor.assert_called_once_with()
        fake_psycopg2.connect.assert_called_once()
        self.assertEqual(dbh.conn, fake_psycopg2)
        self.assertEqual(dbh.cursor, fake_psycopg2)

    @patch('db_handler.psycopg2', MagicMock())
    @patch('db_handler.logging', MagicMock())
    def test_execute_query_with_return(self):
        db_handler.logging = fake_logging = MagicMock()
        dbh = DBHandler(
            'user',
            'password',
            'host',
            'port',
            'database',
        )
        dbh.cursor = fake_cursor = MagicMock()
        dbh.execute_query_with_return('query')
        fake_cursor.execute.assert_called_once_with('query')
        fake_cursor.fetchall.assert_called_once_with()
        fake_logging.info.assert_called_once_with(
            'Query executed successfully')

    @patch('db_handler.psycopg2', MagicMock())
    def test_execute_query_with_no_return(self):
        db_handler.logging = fake_logging = MagicMock()
        dbh = DBHandler(
            'user',
            'password',
            'host',
            'port',
            'database',
        )
        dbh.cursor = fake_cursor = MagicMock()
        dbh.conn = fake_conn = MagicMock()
        dbh.execute_query_with_no_return('query')
        fake_cursor.execute.assert_called_once_with('query')
        fake_conn.commit.assert_called_once_with()
        fake_logging.info.assert_called_once_with(
            'Query executed successfully')







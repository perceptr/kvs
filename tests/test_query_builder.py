import unittest
from query_builder import QueryBuilder


def replace_many_spaces_with_one(string: str) -> str:
    return ' '.join(string.split())


class TestQueryBuilder(unittest.TestCase):
    def setUp(self):
        self.query_builder = QueryBuilder()

    def assert_without_spaces(self, first: str, second: str) -> None:
        self.assertEqual(replace_many_spaces_with_one(first),
                         replace_many_spaces_with_one(second))

    def test_build_create_table_query(self):
        self.assert_without_spaces(
            self.query_builder.build_create_table_query(
                "test_table", ["key", "value"]),
            "CREATE TABLE IF NOT EXISTS test_table "
            "(key VARCHAR(255) PRIMARY KEY, value VARCHAR(255))"
        )

    def test_build_insert_query(self):
        self.assert_without_spaces(
            self.query_builder.build_insert_query(
                "test_table", ["name", "data"], "key", "value"),
            ("INSERT INTO test_table (name, data) SELECT 'key', "
             "'value' WHERE NOT EXISTS ( SELECT name FROM "
             "test_table WHERE name = 'key' )")
        )

    def test_build_where_query_sensitive_case(self):
        self.assert_without_spaces(
            self.query_builder.build_where_query_sensitive_case(
                "test_table", "test_key"),
            "SELECT value FROM test_table WHERE key = 'test_key'"
        )

    def test_build_where_query_insensitive_case(self):
        self.assert_without_spaces(
            self.query_builder.build_where_query_insensitive_case(
                "test_table", "test_key"),
            "SELECT value FROM test_table WHERE LOWER(key) = LOWER('test_key')"
        )

    def test_build_delete_query(self):
        self.assert_without_spaces(
            self.query_builder.build_delete_query("test_table", "test_key"),
            "DELETE FROM test_table WHERE key = 'test_key'"
        )

    def test_build_list_all_keys_query(self):
        self.assert_without_spaces(
            self.query_builder.build_list_all_keys_query("test_table"),
            "SELECT key FROM test_table"
        )

    def test_build_search_by_prefix_query(self):
        self.assert_without_spaces(
            self.query_builder.build_search_by_prefix_query(
                "test_table", "test"),
            "SELECT key FROM test_table WHERE key LIKE 'test%'"
        )

    def test_build_activate_trigger_query(self):
        self.assert_without_spaces(
            self.query_builder.build_activate_trigger_query("test_table"),
            "CREATE OR REPLACE TRIGGER test_tabletrig BEFORE INSERT OR UPDATE "
            "OR DELETE ON test_table FOR EACH ROW EXECUTE PROCEDURE "
            "change_trigger()"
        )

    def test_build_get_commit_log_query(self):
        self.assert_without_spaces(
            self.query_builder.build_get_commit_log_query("test_table"),
            "SELECT * FROM logging.main_log WHERE tabname = 'test_table'"
        )

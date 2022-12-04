class QueryBuilder:
    @staticmethod
    def build_where_query(table: str, key: str) -> str:
        return "SELECT value FROM %s WHERE key = '%s'" % (table, key)

    @staticmethod
    def build_insert_query(table: str, table_fields: list[str], key: str, value: str) -> str:
        return """INSERT INTO %s (%s, %s)
                SELECT '%s', '%s'
                    WHERE
                        NOT EXISTS (
                                    SELECT %s FROM %s WHERE %s = '%s'
            )""" % (table, table_fields[0], table_fields[1], key, value, table_fields[0], table, table_fields[0], key)

    @staticmethod
    def build_create_table_query(table: str, table_fields: list[str]) -> str:
        return """CREATE TABLE IF NOT EXISTS %s (
            %s VARCHAR(255) PRIMARY KEY,
            %s VARCHAR(255)
        )""" % (table, table_fields[0], table_fields[1])

    @staticmethod
    def build_delete_query(table: str, key: str) -> str:
        return "DELETE FROM %s WHERE key = '%s'" % (table, key)

    @staticmethod
    def build_list_all_keys_query(table: str) -> str:
        return "SELECT key FROM %s" % table

    @staticmethod
    def build_search_by_prefix_query(table: str, prefix: str) -> str:
        return "SELECT key FROM %s WHERE key LIKE '%s%%'" % (table, prefix)

    @staticmethod
    def build_activate_trigger_query(table: str) -> str:
        return f"CREATE TRIGGER {table + 'trig'} BEFORE INSERT OR UPDATE OR DELETE ON %s " \
               f"FOR EACH ROW EXECUTE PROCEDURE change_trigger()" % table
    #
    # @staticmethod
    # def build_activate_trigger_if_not_exists_query(table: str) -> str:
    #     return f"CREATE TRIGGER IF NOT EXISTS {table + 'trig'} BEFORE INSERT OR UPDATE OR DELETE ON %s " \
    #            f"FOR EACH ROW EXECUTE PROCEDURE change_trigger()" % table

    @staticmethod
    def build_get_commit_log_query(table: str) -> str:
        return "SELECT * FROM logging.main_log WHERE tabname = '%s'" % table


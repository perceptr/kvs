import os
from db_handler import DBHandler
from query_builder import QueryBuilder
from bucket_handler import BucketHandler
from auth_handler import AuthHandler
from credentials_handler import CredentialsHandler
from bucket_types import BucketTypes
from prettytable import PrettyTable


class KeyValueStorage:
    def __init__(self, storage_name: str, password: str, storage_limit=-1) -> None:
        self.__storage_name = storage_name
        self.__password = password
        self.__database = DBHandler('postgres', 'k4v5s6', '87.239.106.32', '5432', 'postgres')
        self.__auth_handler = AuthHandler(self.__database, self.__storage_name, self.__password)
        self.__query_builder = QueryBuilder()
        self.__check_auth()
        self.__credentials = CredentialsHandler()
        self.__cold_bucket = BucketHandler(self.__credentials.get_cred_by_name("cold_bucket_id"),
                                           self.__credentials.get_cred_by_name("cold_bucket_secret"),
                                           str(BucketTypes.COLD.value),
                                           self.__storage_name)
        self.__hot_bucket = BucketHandler(self.__credentials.get_cred_by_name("hot_bucket_id"),
                                          self.__credentials.get_cred_by_name("hot_bucket_secret"),
                                          str(BucketTypes.HOT.value),
                                          self.__storage_name)

    def create_pair(self, key: str, value: str):
        file_size = os.path.getsize(value)
        fifty_megabytes = 52428800
        self.__database.execute_query_with_no_return(self.__query_builder.build_create_table_query(self.__storage_name,
                                                                                                   ['key', 'value']))
        # TODO manage situation when trigger already exists
        # try:
        #     self.__database.execute_query_with_no_return(self.__query_builder.build_activate_trigger_query(
        #         self.__storage_name
        #     ))
        # except Exception:
        #     pass

        if file_size > fifty_megabytes:
            self.__cold_bucket.upload_file(value)
            value_link = self.__cold_bucket.get_public_link(f"{self.__storage_name}/{value.split('/')[-1]}")
        else:
            self.__hot_bucket.upload_file(value)
            value_link = self.__hot_bucket.get_public_link(f"{self.__storage_name}/{value.split('/')[-1]}")

        query = self.__query_builder.build_insert_query(self.__storage_name, ['key', 'value'], key, value_link)
        self.__database.execute_query_with_no_return(query)

    def get_item(self, key):
        query = self.__query_builder.build_where_query(self.__storage_name, key)
        res = self.__database.execute_query_with_return(query)
        if res:
            return res[0][0]
        else:
            return "No such key-value pair"

    def delete_pair(self, key):
        try:
            value = self.__extract_value_name(self.__database.execute_query_with_return(
                self.__query_builder.build_where_query(self.__storage_name, key)
            )[0][0])
        except IndexError:
            print("No such key-value pair")
            return
        query = self.__query_builder.build_delete_query(self.__storage_name, key)
        self.__database.execute_query_with_no_return(query)

        try:
            self.__hot_bucket.delete_file(f"{self.__storage_name}/{value}")
        except FileNotFoundError:
            self.__cold_bucket.delete_file(f"{self.__storage_name}/{value}")

    def list_all_keys(self):
        query = self.__query_builder.build_list_all_keys_query(self.__storage_name)
        result = self.__database.execute_query_with_return(query)
        return [el[0] for el in result]

    def search_by_prefix(self, prefix):
        query = self.__query_builder.build_search_by_prefix_query(self.__storage_name, prefix)
        result = self.__database.execute_query_with_return(query)
        return [el[0] for el in result]

    def get_commit_log(self):
        query = self.__query_builder.build_get_commit_log_query(self.__storage_name)
        log = self.__database.execute_query_with_return(query)
        table = PrettyTable()
        table.field_names = ["Time", "Table", "Operation", "New value", "Old value"]
        for el in log:
            table.add_row([el[1], el[3], el[4], el[6], el[7]])

        return table

    def get_item_by_value(self, value):
        """
        :param value: value of the key-value pair, as it was named when uploaded from pc
        :param value:
        :return:
        """
        # TODO this is something strange, how to get value by value?

    def __check_auth(self) -> None:
        self.__auth_handler.authenticate()

    @staticmethod
    def __extract_value_name(value):
        return value.split('/')[-1].split('?')[0]

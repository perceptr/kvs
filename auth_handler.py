from db_handler import DBHandler
import hashlib


class AuthHandler:
    def __init__(self, database: DBHandler, storage_name: str, password: str) -> None:
        self.__database = database
        self.__storage_name = storage_name
        self.__hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def __check_if_login_exists(self) -> bool:
        query = "SELECT * FROM auth_table WHERE storage_name = '%s'" % self.__storage_name
        res = self.__database.execute_query_with_return(query)
        if len(res) == 0:
            return False
        return True

    def check_if_password_is_true(self) -> bool:
        query \
            = "SELECT password FROM auth_table WHERE storage_name = '%s' AND password = '%s'" % (self.__storage_name,
                                                                                                 self.__hashed_password)
        res = self.__database.execute_query_with_return(query)
        if len(res) == 0:
            return False
        return True

    def __add_to_auth_table(self) -> None:
        query = "INSERT INTO auth_table (storage_name, password) VALUES ('%s', '%s')" % (self.__storage_name,
                                                                                         self.__hashed_password)
        self.__database.execute_query_with_no_return(query)

    def authenticate(self) -> None:
        if not self.__check_if_login_exists():
            self.__add_to_auth_table()
        else:
            if not self.check_if_password_is_true():
                raise Exception("Wrong password")

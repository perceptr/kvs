import psycopg2
import logging


class DBHandler:
    def __init__(self, user: str, password: str, host: str, port: str, database: str) -> None:
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__database = database
        self.cursor, self.conn = self.__connect_and_get_db_cursor()

    def __connect_and_get_db_cursor(self) -> psycopg2:
        conn = psycopg2.connect(
            user=self.__user,
            password=self.__password,
            host=self.__host,
            port=self.__port,
            database=self.__database
        )

        if conn:
            cursor = conn.cursor()
            return cursor, conn
        try:
            cursor = conn.cursor()
            logging.info("Connection to PostgreSQL DB successful")
        except psycopg2.Error as e:
            logging.error(e)
            return None

        return cursor, conn

    def execute_query_with_return(self, query) -> list:
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        logging.info("Query executed successfully")
        return res

    def execute_query_with_no_return(self, query) -> None:
        self.cursor.execute(query)
        self.conn.commit()
        logging.info("Query executed successfully")


import psycopg2
import logging


class DataBaseReplicator:
    def __init__(self) -> None:
        self.__user = "postgres"
        self.__password = "replica1"
        self.__host = "5.188.142.77"
        self.__port = "5434"
        self.__database = "postgres"
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

    def __execute_replication_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        logging.info(f"Query: {query} replicated successfully")

    def replicate(self, func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            self.__execute_replication_query(args[1])
            return res
        return wrapper

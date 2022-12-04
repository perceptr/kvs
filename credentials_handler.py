import sqlite3


class CredentialsHandler:
    def __init__(self):
        self.__conn = sqlite3.connect("credentials.db")
        self.__cursor = self.__conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cred_name TEXT NOT NULL,
            cred_value TEXT NOT NULL
        )""")
        self.__conn.commit()

    def insert_cred(self, cred_name: str, cred_value: str) -> None:
        self.__cursor.execute("INSERT INTO credentials (cred_name, cred_value) VALUES (?, ?)", (cred_name, cred_value))
        self.__conn.commit()

    def get_cred_by_name(self, cred_name: str) -> str:
        self.__cursor.execute("SELECT cred_value FROM credentials WHERE cred_name = ?", (cred_name,))
        return self.__cursor.fetchone()[0]

    def __delete_cred_by_name(self, cred_name: str) -> None:
        """
        This method is for one's convenience, it is not used in the program
        :param cred_name:
        :return:
        """
        self.__cursor.execute("DELETE FROM credentials WHERE cred_name = ?", (cred_name,))
        self.__conn.commit()

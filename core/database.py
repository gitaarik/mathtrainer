from pysqlite2 import dbapi2 as sqlite
from core.exceptions import DatabaseError

class Database:
    """
    Manages connections and provides functions to communicate with the database.
    """

    __shared_state = {}

    def __init__(self):
        # ensure every instance of this object shares
        # the same connection and cursor object
        self.__dict__ = self.__shared_state

    def open(self, file):
        """
        Open the connection to the database.

        Establishes the connection to the database through a sqlite file.
        If it fails it will raise a DatabaseError exception.
        """

        try:
            self.connection = sqlite.connect(file)
        except sqlite.OperationalError:
            raise DatabaseError('Could not open database file. ' +
            'Do I have write access?')

        self.cursor = self.connection.cursor()

    def close(self):
        """
        Close the connection to the database.
        """
        self.connection.close()

    def query(self, query, *args):
        """
        Execute a query on the database and return the result.
        """
        r = self.cursor.execute(query, args)
        self.connection.commit()
        return r

    def fetchall(self, query, *args):
        """
        Execute SELECT query and fetch all of the rows and return them.
        """
        self.query(query, *args)
        return self.cursor.fetchall()

    def fetchone(self, query, *args):
        """
        Execute SELECT query and fetch first row and return it.
        """
        self.query(query, *args)
        return self.cursor.fetchone()

    def fetchcol(self, query, *args):
        """
        Execute SELECT query and fetch first column of first row and return it.
        """
        return self.fetchone(query, *args)[0]

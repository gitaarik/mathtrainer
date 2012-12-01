class StopGame(Exception):
    pass

class DatabaseError(Exception):
    """
    An exception occured in the database.

    Will posibly contain a message which describes the cause
    of the database error, found in 'DatabaseError.message'.

    """

    def __init__(self, message=''):
        """
        Init the DatabaseError

        Keyword arguments:
        message -- A message that describes the cause of the database error.

        """
        self.message = message

import argparse
from os.path import dirname
from time import time
from database import Database
from core.game import Game
from core.exceptions import (StopGame, DatabaseError)
from core.results import Results
from core.highscores import Highscores

databasefile = dirname(dirname(__file__)) + '/database.sqlite'

class Main:
    """
    Main class of the program.

    Use the start() method of this class to start up this program.

    """

    def start(self):
        """
        Starts the program.

        Will interpret the commandline and do stuff according to that.

        """

        self.init_database()
        self.parse_command()

        if self.args.clearhs:
            sure = raw_input('Are you sure you '
            'want to clear all the highscores? y/n\n')
            if sure == 'y' or sure == 'Y':
                Highscores().clear()
                exit('Highscores have been cleared.')
            else:
                exit('Highscores are retained.')

        if self.args.highscores:
            self.show_highscores()
        else:
            self.run_game()

        self.close_database()

    def init_database(self):
        """
        Initiate the database class.

        Will open a sqlite database file and
        create tables if they are not present yet.

        """

        self.database = Database()

        try:
            self.database.open(databasefile)
        except DatabaseError as error:
            print 'The database gave an error:\n {0}'.format(error.message)
            exit()

        self.database.query('''CREATE TABLE IF NOT EXISTS
        highscores (user VARCHAR(255), level TINYINT,
        questions SMALLINT, mistakes SMALLINT, time FLOAT)''')

    def close_database(self):
        """
        Close the database.

        Will close off the database connections
        opened by the init_dtabase() method.

        """
        self.database.close()

    def run_game(self):
        """
        Run the game.

        Will run the game this program is all about. After the game it will
        collect results and possibly list the player in the Highscores list.

        """

        g = Game(self.args.level, self.args.questions)
        start_time = time()

        try:
            g.run()
        except StopGame:
            print '\nbye!'
            exit()

        endtime = time() - start_time

        r = Results(self.args.level, self.args.questions,
        g.mistakes, endtime)
        r.print_results()

        Highscores().new(r)

    def show_highscores(self):
        """
        Show the highscores of the game.

        There are different highscore lists per level and number of questions.

        """
        Highscores().print_top(self.args.level, self.args.questions)

    def parse_command(self):
        """
        Parses the command the program is booted with.

        Sets the provided arguments in class variable 'self.args'.

        """

        parser = argparse.ArgumentParser(description='Math trainer! A simple ' +
        'program that helps you bump up your arithmetic!')
        parser.add_argument('-l', '--level', default=1, type=int, help='The ' +
        'level of difficulty.', choices=[1, 2, 3, 4, 5])
        parser.add_argument('-q', '--questions', default=20, type=int, help=
        'The amount of questions.', choices=[5, 10, 20, 50])
        parser.add_argument('-s', '--highscores', action='store_true',
        help='Show the highscores.')
        parser.add_argument('-c', '--clearhs', action='store_true',
        help='Clear the highscores.')

        self.args = parser.parse_args()

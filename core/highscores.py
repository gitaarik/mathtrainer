from database import Database

class Highscores:
    """
    Manages highscores of played games.
    """

    # The limit of the highscores list
    limit = 10

    def __init__(self):
        self.database = Database()

    def new(self, results):
        """
        Submit a new highscore.

        If the score is high enough, it will ask for a
        name which will be used for the highscore listing.

        Keyword arguments:
        results -- A results object, instance of class Results (results.py)

        """

        higher_scores = self.get_higher_scores(results)

        if(higher_scores < self.limit):

            print ('\nYou reached #{0} in the highscores! '
            'Enter your name:').format(higher_scores + 1)

            try:
                name = self.get_name()
            except (KeyboardInterrupt, EOFError):
                print '\nDon\'t even wanna be in the highscores huh? Tss...'
                return

            self.insert_high_score(name, results)

    def get_name(self):
        """
        Get a name of the player.

        Will ask for a name, if the player enters
        nothing (or whitespace), it will ask again.

        """

        first = True
        name = ''

        while name is '':
            if first is False:
                print 'That\'s not a valid name! Try again:'
            name = raw_input().strip(' \t\n\r')
            first = False

        return ' '.join(name.split())

    def print_top(self, level, questions):
        """
        Print the top highscores.
        
        Will print a nice overview of the highest scores.

        Keyword arguments:
        level -- The level of the highscores list
        questions -- The number of questions of the highscores list

        """

        print (
            '\n'
            '{2}.-- Highscores --.\n'
            '{2}|                |\n'
            '{2}|    level: {0:<5}|\n'
            '{2}|  questions: {1:<3}|\n'
            '{2}|                |\n'
            '{2}\'----------------\'\n'
        ).format(level, questions, ' '*7)

        top = self.get_top(level, questions)
        top = [(
            str(i + 1),
            row[0],
            str(row[3]),
            str(round(float(row[4]), 3))
        ) for i, row in enumerate(top)]

        # header of the highscores table
        top[:0] = [tuple(['-'*11])*4]
        top[:0] = [('#', 'User', 'Mistakes', 'Time')]

        print '\n'.join((
            '{0:2} {1:11} {2:11} {3:11}'.format(
                row[0][:2],
                row[1][:11],
                row[2][:11],
                row[3][:11]
            )
        ) for row in top) + '\n'

    def get_top(self, level, questions):
        """
        Get the top highscores.

        Keyword arguments:
        level -- The level of the highscores listing.
        questions -- The amount of questions of the highscores listing.

        """
        return self.database.fetchall('''SELECT * FROM highscores
        WHERE level = ? AND questions = ?
        ORDER BY time, mistakes ASC
        LIMIT ?''', level, questions, self.limit)

    def get_higher_scores(self, results):
        """
        Count the scores that are higher than this one.

        Keyword arguments:
        results -- A results object, instance of class Results (results.py)
        
        """

        return self.database.fetchcol('''
        SELECT COUNT(*) FROM highscores
        WHERE level = ? AND questions = ?
        AND time < ?''',
        results.level, results.questions,
        results.time)

    def insert_high_score(self, name, results):
        """
        Insert new highscore.

        Keyword arguments:
        name -- The name of the player that reached the highscore.
        results -- A results object, instance of class Results (results.py)
        
        """

        self.database.query('''INSERT INTO highscores
        (user, level, questions, mistakes, time)
        VALUES (?, ?, ?, ?, ?)''',
        name, results.level, results.questions,
        results.mistakes, results.time)

    def clear(self):
        self.database.query('DELETE FROM highscores')

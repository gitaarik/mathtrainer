class Results:
    """
    Collects results from a played game.
    """

    def __init__(self, level, questions, mistakes, time):
        """
        Init the results object.

        Keyword arguments:
        level -- The level of the game.
        questions -- The number of questions of the game.
        mistakes -- The mistakes the player made during the game.
        time -- The time the player took to finish te game.

        """

        self.level = level
        self.questions = questions
        self.mistakes = mistakes
        self.time = time 

    def print_results(self):
        """
        Print the results.

        Prints the results in a nice way, for example:

        Results:
         level: 1
         questions: 20
         mistakes: 3
         time: 35.351s

        """

        minutes = self.time / 60
        seconds = self.time % 60

        print ('Results:\n'
        ' level: {0:d}\n'
        ' questions: {0:d}\n'
        ' mistakes: {0:d}').format(self.level, self.questions, self.mistakes)

        if minutes >= 1:
            print ' time: {0:0>2.0f}:{1:0>6.3f}s'.format(minutes, seconds)
        else:
            print ' time: {0:0>6.3f}s'.format(seconds)

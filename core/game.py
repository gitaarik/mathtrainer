import decimal
from collections import deque
import validate
from ._questions import Questions
from .exceptions import StopGame

class Game:
    """
    A game that askes a number of random arithmetic questions and prints out the
    stats of the played game after the user answered all the questions correct.
    """

    def __init__(self, level, number_questions, uniq_question_limit = 50):
        """
        Init the game.

        Keyword arguments:
        level -- Level of difficulty
        number_questions -- Number of questions asked
        uniq_question_limit -- The number of questions that should be
                               remembered. This is used for the unique-
                               ness of upcomming questions.

        """
        self.level = level
        self.number_questions = number_questions
        self.asked_questions = deque([None])
        self.uniq_question_limit = 50
        self.questions = Questions(level)
        self.mistakes = 0

    def run(self):
        """
        Run the game.
        
        Returns the mistakes the user made.
        
        """

        for i in range(self.number_questions):
            self._ask_question()


    def _ask_question(self):
        """
        Ask a question.
        
        Prints out a question to the screen and
        prompts the user to enter an answer.
        
        """

        question = self._get_question()
        calculation = question[0] + question[1] + question[2]
        correct_answer = eval(calculation)
        correct = False

        while correct == False:

            print '\n' + calculation + '\n'
            user_answer = self._get_user_answer()

            if (
                validate.floatnum(user_answer) and
                decimal.Decimal(user_answer) == decimal.Decimal(correct_answer)
            ):
                print 'correct!\n'
                correct = True
            else:
                print 'wrong!\n'
                self.mistakes += 1

    def _get_user_answer(self):
        """
        Get answer from user by prompting the user.
        """

        try:
            user_answer = raw_input()
        except (KeyboardInterrupt, EOFError):
            self._stop()

        if user_answer in ['exit', 'quit', 'stop']:
            self._stop()

        return user_answer

    def _stop(self):
        """
        Raise StopGame exception.
        """
        raise StopGame

    def _get_question(self):
        """
        Get unique question.

        The unique-ness is based on a number of remembered questions,
        which can be configured when creating this class.

        """

        # self.asked_questions' first item is None so
        # the while will work the first time it enters.
        question = None

        while question in self.asked_questions:
            question = self.questions.get_question()
        
        self.asked_questions.append(question)

        # Only remember last self.uniq_question_limit questions,
        # in case too much (or only) duplicates show up.
        if len(self.asked_questions) > self.uniq_question_limit:
            self.asked_questions.popleft()

        return question

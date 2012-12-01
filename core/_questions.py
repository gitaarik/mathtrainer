from random import randint

class Questions:
    """
    Questions that can be used in a game.
    """

    def __init__(self, level):
        """
        Init the questions.

        Keyword arguments:
        level -- Level of difficulty

        """
        self.level = level

    def get_question(self):
        """
        Generates a question and returns it.

        The question will be formatted as a list consisting of three
        strings that contain a number, an operator and another number.

        Example:
        
        >>> q.get_question()
        ['3', '*', '5']

        You should interpret this question of course as:
        3*5
        Where the correct answer would be:
        15

        """

        # Determin question type
        # 0 = addition (+)
        # 1 = substraction (-)
        # 2 = multiplication (*)
        # 3 = division (/)
        question_type = randint(0, 3)
        # The numbers for the question
        numbers = []

        if question_type < 2:
            numbers.append(self._get_number_add_sub())
            numbers.append(self._get_number_add_sub())
        else:
            numbers.append(self._get_number_mul_div())
            numbers.append(self._get_number_mul_div())

        if question_type == 0:
            operator = '+'
        elif question_type == 1:
            operator = '-'
            # Ensure we don't get below zero
            if numbers[1] > numbers[0]:
                numbers[0], numbers[1] = numbers[1], numbers[0]
        elif question_type == 2:
            operator = '*'
        elif question_type == 3:
            operator = '/'
            # Ensure we don't get fractions
            numbers[0] *= numbers[1]

        return [str(numbers[0]), operator, str(numbers[1])]

    def _get_number_add_sub(self):
        """
        Get a random number for an addition or substraction question.
        """
        return randint(1, pow(2, self.level-1)*25)

    def _get_number_mul_div(self):
        """
        Get a random number for an multiplication or division question.
        """
        return randint(1, self.level*4)

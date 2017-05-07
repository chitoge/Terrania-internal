# base classes for question model
from abc import ABCMeta, abstractmethod

class MultiChoiceQuestion(object):
    def __init__(self, type_str, choices, correct_answer):
        self.question_type = type_str
        self.choices = choices
        self.correct_answer = correct_answer

    def validate(self, answer):
        return (self.correct_answer == answer)

class BaseQuestionGenerator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, used_list, candidates, language):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def view(self, question):
        pass

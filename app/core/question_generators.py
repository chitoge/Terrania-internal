# question generator classes
from questions import *
import random

class RandomMultiChoiceGenerator:
    def __init__(self, previous_answers, candidates, language, data_tag, generator_tag, answer_gen_fn):
        self.language = language
        self.data_tag = data_tag
        self.generator_tag = generator_tag
        # generate an index in range [0..3] for the answer, given a list of choices
        self.answer_gen_fn = answer_gen_fn
        # filter duplicated candidates
        if (len(previous_answers) > 0):
            to_be_removed = filter(lambda x: x[1] == data_tag, previous_answers)
        else:
            to_be_removed = []
        self.candidates = list(set(candidates) - set(to_be_removed))

    def generate(self):
        # if there are less than 4 candidates left, we deny the request
        if (len(self.candidates) < 4):
            raise IndexError('Less than 4 candidates remained for a multiple choice question')
        # is it supposed to be cryptographically secure?
        # maybe, but in other cases, not this case
        choices = random.sample(self.candidates, 4)
        # generate answer from this
        answer = self.answer_gen_fn(choices)
        # return a tuple (question, type of data used)
        return MultiChoiceQuestion(self.generator_tag, choices, answer), self.data_tag

    def check_generator_view_tag(self, question):
        # sanity check for the right type of question
        if (question.question_type != self.generator_tag):
            raise TypeError('Trying to view a question of wrong type')
        pass

class Flag2CountryGenerator(BaseQuestionGenerator):
    def __init__(self, used_list, candidates, language):
        self.generator = RandomMultiChoiceGenerator(used_list, candidates, language, 'flag', 'flag2country', lambda x: random.randint(0, 3))

    def generate(self):
        return self.generator.generate()

    def view(self, question):
        self.generator.check_generator_view_tag(question)
        # TODO: apply i18n & load image
        q = 'What country is this flag from?'
        img_data = load_flag(question.choices[question.correct_answer].country_code)
        return dict(question=dict(type='captioned_image', data=img_data, title=q), answers=[dict(type='text', data=s.name) for s in question.choices])

class Country2FlagGenerator(BaseQuestionGenerator):
    def __init__(self, used_list, candidates, language):
        self.generator = RandomMultiChoiceGenerator(used_list, candidates, language, 'flag', 'country2flag', lambda x: random.randint(0, 3))

    def generate(self):
        return self.generator.generate()

    def view(self, question):
        self.generator.check_generator_view_tag(question)
        # TODO: apply i18n & load image
        q = 'What is the flag of %s?' % question.choices[question.correct_answer].name
        img_data = ''
        return dict(question=dict(type='text', data=q), answers=[dict(type='image', data=load_flag(c.country_code)) for c in question.choices])

class Capital2CountryGenerator(BaseQuestionGenerator):
    def __init__(self, used_list, candidates, language):
        self.generator = RandomMultiChoiceGenerator(used_list, candidates, language, 'capital', 'capital2country', lambda x: random.randint(0, 3))

    def generate(self):
        return self.generator.generate()

    def view(self, question):
        self.generator.check_generator_view_tag(question)
        # TODO: apply i18n & load image
        q = '%s is the capital of...' % question.choices[question.correct_answer].capital
        return dict(question=dict(type='text', data=q), answers=[dict(type='text', data=c.name) for c in question.choices])

class Country2CapitalGenerator(BaseQuestionGenerator):
    def __init__(self, used_list, candidates, language):
        self.generator = RandomMultiChoiceGenerator(used_list, candidates, language, 'capital', 'country2capital', lambda x: random.randint(0, 3))

    def generate(self):
        return self.generator.generate()

    def view(self, question):
        self.generator.check_generator_view_tag(question)
        # TODO: apply i18n & load image
        q = 'What is the capital of %s?' % question.choices[question.correct_answer].name
        return dict(question=dict(type='text', data=q), answers=[dict(type='text', data=c.capital) for c in question.choices])
# question generator classes
from questions import *
import random
from ..models.i18n import Translation

def load_flag(country):
    # don't LFI me!
    with open('data/flags/%s.png' % country.lower()) as f:
        # return PNG Base64
        return f.read().encode('base64')

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
        to_be_removed = set(x[0] for x in to_be_removed)
        # wish it could be simpler
        new_candidates = []
        for candidate in candidates:
            if (candidate.country_code not in to_be_removed):
                new_candidates.append(candidate)
        self.candidates = new_candidates

    def generate(self):
        # if there are less than 4 candidates left, we deny the request
        if (len(self.candidates) < 4):
            raise IndexError('Less than 4 candidates remained for a multiple choice question')
        # is it supposed to be cryptographically secure?
        # maybe, but in other cases, not this case
        choices = random.sample(self.candidates, 4)
        # generate answer from this
        answer = self.answer_gen_fn(choices)
        # translate choices to chosen language
        choices = map(lambda x: Translation.translate(x, self.language), choices)
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

    def view(self, question, overrides=False):
        # overriding doesn't matter here!
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

    def view(self, question, overrides=False):
        self.generator.check_generator_view_tag(question)
        # TODO: apply i18n & load image
        #q = 'What is the flag of %s?' % question.choices[question.correct_answer].name
        # client hack
        q = question.choices[question.correct_answer].name
        img_data = ''
        return dict(question=dict(type='text', data=q), answers=[dict(type='image', data=load_flag(c.country_code)) for c in question.choices])

class Capital2CountryGenerator(BaseQuestionGenerator):
    def __init__(self, used_list, candidates, language):
        self.generator = RandomMultiChoiceGenerator(used_list, candidates, language, 'capital', 'capital2country', lambda x: random.randint(0, 3))

    def generate(self):
        return self.generator.generate()

    def view(self, question, overrides=False):
        self.generator.check_generator_view_tag(question)
        # TODO: apply i18n & load image
        #q = '%s is the capital of...' % question.choices[question.correct_answer].capital
        # client hack
        q = question.choices[question.correct_answer].capital
        return dict(question=dict(type='text', data=q), answers=[dict(type='text', data=c.name) for c in question.choices])

class Country2CapitalGenerator(BaseQuestionGenerator):
    def __init__(self, used_list, candidates, language):
        self.generator = RandomMultiChoiceGenerator(used_list, candidates, language, 'capital', 'country2capital', lambda x: random.randint(0, 3))

    def generate(self):
        return self.generator.generate()

    def view(self, question, overrides=False):
        self.generator.check_generator_view_tag(question)
        # TODO: apply i18n & load image
        # q = 'What is the capital of %s?' % question.choices[question.correct_answer].name
        # client hack
        q = question.choices[question.correct_answer].name
        return dict(question=dict(type='text', data=q), answers=[dict(type='text', data=c.capital) for c in question.choices])

class MixedQuestionsGenerator(BaseQuestionGenerator):
    def __init__(self, used_list, candidates, language):
        self.used_list = used_list
        self.candidates = candidates
        self.language = language
        # randomly choose from available generators
        possible_generators = list((set(generators.values()) | set(private_generators)) - set([MixedQuestionsGenerator]))
        self.generator = random.choice(possible_generators)(self.used_list, self.candidates, self.language)

    def generate(self):
        question, data_tag = self.generator.generate()
        # will insert an attribute for its original generator
        # stored as name
        for g_name in generators:
            if (isinstance(self.generator, generators[g_name])):
                setattr(question, 'generator_name', g_name)
                break
        if (not hasattr(question, 'generator_name')):
            raise TypeError("Can't find a generator name associated to given generator")
        return question, data_tag

    def view(self, question):
        # restore 
        return generators[question.generator_name]([], [], self.language).view(question)

generators = {
    'flag2country': Flag2CountryGenerator,
    'country2flag': Country2FlagGenerator,
    'capital2country': Capital2CountryGenerator,
    'country2capital': Country2CapitalGenerator,

    # mix 'em all!
    'mixed': MixedQuestionsGenerator
}

private_generators = []
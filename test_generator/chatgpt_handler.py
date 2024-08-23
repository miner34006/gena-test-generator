import json
import os
from copy import deepcopy

from openai import OpenAI

from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite

PROMPT = """
    There is a list of test cases in JSON format.

    The fields mean the following:
        - description - test description;
        - is_positive - whether the test is positive or negative;
        - subject - an existing name for the test;

    Compose the names of these test cases following these rules:
        - the response should contain the names of the tests in text format, each name should start on a new line without any symbols except test name;
        - the order of the tests should be preserved;
        - the names of the tests should be in English and use simple English constructions;
        - the names should be in a consistent style;
        - negative tests should start with try to;
        - the name should not be longer than 12 words;
        - if the initial list already contains a test with subject, the remaining tests should use similar style and grammatical constructions;
        - to specify certain test conditions (e.g., when an invalid body parameter is passed) use 'when' or 'with', e.g. "with invalid body";
        - if the test object contains the "subject" key, the answer should return to the same test name as in the "subject" field even if the test is negative and does not contain try to;
        - the names should not contain ordinal numbers, quotation marks, dashes and any symbols;
        - the names should be in lower case;
        - words in a names must be separated by spaces;

    Test cases:\n
    """


class ChatGPTHandler:
    def __init__(self, key: str = None, base_url: str = None) -> None:
        key = key or os.environ.get('OPENAI_API_KEY', '')
        base_url = base_url or os.environ.get('OPENAI_URL', '')
        self.client = OpenAI(api_key=key, base_url=base_url)

    def __test_cases_as_json(self, test_cases: list[TestScenario]) -> list[dict]:
        cases = [{
            'description': t.description,
            'is_positive': t.is_positive,
            'subject': t.subject
        } for t in test_cases]
        return cases

    def update_suite(self, suite: Suite) -> Suite:
        original_cases = suite.test_scenarios
        ai_updated_cases = self.__generate_test_subjects(deepcopy(original_cases))

        while True:
            print("\n🔍 Будут использованы следующие названия тестов:")
            for i, test_case in enumerate(ai_updated_cases):
                print(f"{i+1}. {test_case.subject}")
            print()

            print("Введите номера тестов для изменения через запятую (например, '1,3,5') или 'q' для продолжения:")
            user_input = input(">  ")
            print()

            if user_input.lower() == 'q':
                break

            try:
                need_regeneration = False
                indices = [int(i.strip()) - 1 for i in user_input.split(',')]
                for index in indices:
                    if index < 0 or index >= len(ai_updated_cases):
                        raise ValueError('Невалидный индекс теста')

                    print(f"🔍 Если вы хотите перегенерировать остальные названия на основе измененных данных, "
                          f"отправьте первым символом знак '!'.\n\nВведите новое название для теста {index + 1}:")
                    new_subject = input(">  ")
                    print()

                    if new_subject.startswith('!'):
                        need_regeneration = True
                        new_subject = new_subject[1:]
                    if new_subject:
                        original_cases[index].subject = new_subject
                        ai_updated_cases[index].subject = new_subject
                    else:
                        raise ValueError('Invalid subject received, please try again...')

                if need_regeneration:
                    ai_updated_cases = self.__generate_test_subjects(original_cases)

            except (ValueError, IndexError):
                print("⚠️ Некорректный ввод, попробуйте снова.")

        suite.test_scenarios = ai_updated_cases
        return suite

    def __generate_test_subjects(self, test_cases: list[TestScenario]) -> list[TestScenario]:
        print('⌛ Генерация названий тестов с использованием ChatGPT...')
        prompt = PROMPT + json.dumps(self.__test_cases_as_json(test_cases))

        response = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0.5,
            messages=[
                {"role": "system", "content": "Ты QA инженер, помогающий генерировать названия тестов."},
                {"role": "user", "content": prompt},
            ]
        )
        if not response.choices[0].message.content:
            raise Exception("Error while generating test names")
        subjects = response.choices[0].message.content.split('\n')
        subjects = [s.strip() for s in subjects if s.strip()]

        for i, case in enumerate(test_cases):
            case.subject = subjects[i]

        return test_cases

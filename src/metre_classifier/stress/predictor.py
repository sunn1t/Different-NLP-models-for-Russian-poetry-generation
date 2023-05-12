# Based on: rupo
# Source: https://github.com/IlyaGusev/rupo

from typing import List

from src.metre_classifier.stress.word import Stress
from src.metre_classifier.stress.dict import StressDict
from src.metre_classifier.util.preprocess import count_vowels, get_first_vowel_position
from src.settings import ZALYZNYAK_DICT

from russ.stress.predictor import StressPredictor

class DictStressPredictor():
    def __init__(self, language="ru", raw_dict_path=None, trie_path=None,
                 zalyzniak_dict=ZALYZNYAK_DICT):
        self.stress_dict = StressDict(language, raw_dict_path=raw_dict_path, trie_path=trie_path,
                                      zalyzniak_dict=zalyzniak_dict)

    def predict(self, word: str) -> List[int]:
        """
        Определение ударения в слове по словарю. Возможно несколько вариантов ударения.
        :param word: слово для простановки ударений.
        :return stresses: позиции букв, на которые падает ударение.
        """
        stresses = []
        if count_vowels(word) == 0:
            # Если гласных нет, то и ударений нет.
            pass
        elif count_vowels(word) == 1:
            # Если одна гласная, то на неё и падает ударение.
            stresses.append(get_first_vowel_position(word))
        elif word.find("ё") != -1:
            # Если есть буква "ё", то только на неё может падать ударение.
            stresses.append(word.find("ё"))
        else:
            # Проверяем словарь на наличие форм с ударениями.
            stresses = self.stress_dict.get_stresses(word, Stress.Type.PRIMARY) +\
                       self.stress_dict.get_stresses(word, Stress.Type.SECONDARY)
            if 'е' not in word:
                return stresses
            # Находим все возможные варинаты преобразований 'е' в 'ё'.
            positions = [i for i in range(len(word)) if word[i] == 'е']
            beam = [word[:positions[0]]]
            for i in range(len(positions)):
                new_beam = []
                for prefix in beam:
                    n = positions[i+1] if i+1 < len(positions) else len(word)
                    new_beam.append(prefix + 'ё' + word[positions[i]+1:n])
                    new_beam.append(prefix + 'е' + word[positions[i]+1:n])
                    beam = new_beam
            # И проверяем их по словарю.
            for permutation in beam:
                if len(self.stress_dict.get_stresses(permutation)) != 0:
                    yo_pos = permutation.find("ё")
                    if yo_pos != -1:
                        stresses.append(yo_pos)
        return stresses


class CombinedStressPredictor():
    def __init__(self, language="ru", raw_stress_dict_path=None,
                 stress_trie_path=None, zalyzniak_dict=ZALYZNYAK_DICT):
        self.rnn = StressPredictor()
        self.dict = DictStressPredictor(language, raw_stress_dict_path, stress_trie_path, zalyzniak_dict)

    def predict(self, word: str) -> List[int]:
        stresses = self.dict.predict(word)
        if len(stresses) == 0:
            return self.rnn.predict(word)
        else:
            return stresses

import numpy as np
import pandas as pd

class Dictionary:
    def __init__(self, dict_dir):
        '''
         Hash Table or dict()
        '''
        self.data = pd.read_csv(dict_dir, encoding="UTF8")

        print("Building Dictionary from ", dict_dir)
        self._word2idx = {}
        self._idx2word = {}
        for i in range(len(self.data)):
            self._word2idx[self.data.iloc[i]['word']] = self.data.iloc[i]['index']
            self._idx2word[self.data.iloc[i]['index']] = self.data.iloc[i]['word']

    @property
    def dict_len(self):
        return len(self._word2idx)

    @property
    def sign(self):
        return ['，', '？', '！', '、', '—',
                '“', '”', '；', '。', '|', '{', '}',
                '《', '》', '.', ',', '<', '>', ':', '：', '）', '（']

    def word2idx(self, word):
        try:
            return self._word2idx[word]
        except KeyError:
            return self._word2idx["UNK"]

    def idx2word(self, idx):
        try:
            return self._idx2word[idx]
        except KeyError:
            return "UNK"


class City(Dictionary):
    def __init__(self, dict_dir):
        '''

        law/dict/places.csv
        five columns
        index	word	region	area	province
        序号     城市名   地区     大区    省份
        4       上海市   苏皖沪    东区    上海市

        '''
        super().__init__(dict_dir)

    def idx2city(self, idx):

        return self.idx2word(idx)

    def city2idx(self, city):

        return self.word2idx(city)

    def city2province(self, city):

        return 0

    def city2region(self, city):

        return 0

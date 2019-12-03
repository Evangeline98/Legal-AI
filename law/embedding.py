import numpy as np
import pandas as pd
import jieba
import law.utils
import law


# Base Model
class Embedding:
    def __init__(self, dictionary, jieba_dict):
        '''
        :param:
            dictionary
            jieba_dit law/dict/jiebadict.txt
        '''
        self.dictionary = dictionary
        jieba.load_userdict(jieba_dict)
        '''
        For hyper-parameters
        '''

    def transform(self, string, plantiff='', defendant='', third_party=''):
        '''
        entity identification.

        '地名': PLA
        '原告': PLT
        '被告': DFD
        '第三人': THP
        '标点符号': delete
        '数字': NUMBER

        :param:
            string str()
            plantiff str()
            defendant str()
            third_party str()

        :output:
            transformed string
        '''

        # Replace 原告名字
        # if not plantiff: # Make sure it's not none
        for each_name in plantiff.split('、'):
            string = str(string).replace(each_name, 'PLT')

        # Replace 被告名字
        # if not defendant:
        for each_name in defendant.split('、'):
            string = str(string).replace(each_name, 'DFD')

        # Replace 第三人名字
        # if not plantiff:
        for each_name in plantiff.split('、'):
            string = str(string).replace(each_name, 'THP')


        for each_sign in self.dictionary.sign:
            # The extra str is to make sure that replace would work
            string = str(string).replace(each_sign, '')

        #"DATE"

        string = law.utils.change_date_to_DATE(string)

        string = law.utils.change_money_to_MONEY(string)

        return string

    def cut(self, transformed):
        '''

        '''
        cutted = [each_word for each_word in jieba.cut(transformed)]
        return cutted

    def map(self, cutted):
        '''

        '''
        mapped = []
        for each_word in cutted:
            mapped.append(self.dictionary.word2idx(each_word))
        return mapped

    def pad(self, mapped, pad=2000):
        '''
        After mapping to num_list, we need to do padding,
        such that we would be able to use all models without getting trouble with
        dimensions.
        Input:
            mapped num_list
            pad              lenth you want to pad, set default = 2000
        output: padded num_list
        '''
        if len(mapped) >= 2000:
            return mapped[:2000]
        elif len(mapped) < 2000:
            _mapped = mapped.copy()
            _mapped.extend([0] * (2000 - len(_mapped)))
            return _mapped

    def embed(self, string, plantiff='', defendant='', third_party='', pad = 2000):
        '''
        输入一段文字，对这一段文字进行分词+mapping处理
        :param:
        str():string
            pad:
        :return:
            np.array() 输出的embedding

        '''
        # 首先调用transform进行预处理
        transformed = self.transform(string, plantiff, defendant, third_party)
        # print(transformed)
        # 分词
        cutted = self.cut(transformed)
        # print(cutted)
        # 然后进行map操作变为num_list
        num_list = self.map(cutted)
        # print(num_list)
        padded_list = self.pad(num_list, pad=pad)

        # 进行embed操作每个不同方法不同
        embedded = padded_list
        return embedded

    def embed_pandas(self, df, targets, plantiff="plantiff",
                     defendant="defendant", third_party="third_party", pad=2000):
        '''
        dataframe,
        targets
        '''
        embedded_list = []
        for i in range(df.shape[0]):
            if i % 20 == 0:
                print("Doing", i, ". Total", df.shape[0])
            each_row_embed = []
            if type(targets) == str:
                # 说明只有一个输入的str
                embedded_list.append(self.embed(string=df.iloc[i][targets],
                                                     plantiff=df.iloc[i][plantiff],
                                                     defendant=df.iloc[i][defendant],
                                                     third_party=df.iloc[i][third_party]))
            else:
                # 多target模式
                for each_target in targets:
                    each_row_embed.append(self.embed(string=df.iloc[i][each_target],
                                                         plantiff=df.iloc[i][plantiff],
                                                         defendant=df.iloc[i][defendant],
                                                         third_party=df.iloc[i][third_party]))
                embedded_list.append(each_row_embed)
        return np.array(embedded_list)


class word_freq(Embedding):
    def __init___(self, dict_dir, jieba_dict):

        super().__init__(dict_dir, jieba_dict)

    def embed(self, string, plantiff, defendant, third_party):

        return 0


class char_freq(Embedding):
    def __init__(self, dict_dir, jieba_dict):

        super().__init__(dict_dir, jieba_dict)
        pass


class TFIDF(Embedding):
    '''
    This class is updated by Klaus.
    '''

    def __init__(self, dict_dir, jieba_dict):

        super().__init__(dict_dir, jieba_dict)

        pass


class BERT(Embedding):
    def __init__(self, dict_dir, jieba_dict):
        '''
        TODO
        BERT - Bidirectional Encoder Representations from Transformers
        https://arxiv.org/pdf/1810.04805.pdf


        - common words in the model
        - other words are built from character

        '''
        super().__init__(dict_dir, jieba_dict)

        pass

import sklearn


class Model:
    def __init__(self, *arg):
        '''

        centralization and standardization

        input parameters
        '''

    def fit(self, X, y, *arg, **kwargs):
        '''

        :param:
                X: X
                y：y
                *arg: other
        '''
        pass

    def predict(self, new_X, *arg, **kwargs):
        '''

        :param:
                new_X
        :return:
                predicted_y
        '''
        pass

    def store(self, path='../.cache/'):
        '''
        store model
        into json/npy

        '''

        pass

    def read(self, dir='../.cache/xxx.m'):
        '''
        read model
        '''
        pass

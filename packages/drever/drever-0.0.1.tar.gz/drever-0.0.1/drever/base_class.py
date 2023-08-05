'''
Created on Apr 16, 2019

@author: baumannt
'''

# from abc import ABC, abstractmethod
from drever.file_handler import FileHandler


class Drever(FileHandler):
    '''
    This is the drever base class. New Drever classes needs to be derived from
    this base class with an overwritten run method.
    '''

    DEFAULT_PARAMS = {}

    def __init__(self, params=None):
        '''
        Constructor
        '''
        self.params = self.DEFAULT_PARAMS if params is None else params

    def run(self, data):
        '''
        The default algorithm is a simple data bypass. This methode needs to
        be overwritten.
        '''
        return data

    def set_params(self, params):
        '''
        Parameter Setter
        '''
        self.params = params

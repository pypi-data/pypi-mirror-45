#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Kernel:
    def __init__(self):
        self.setup()

    def setup(self):
        pass

    def transform(self, value):
        raise NotImplementedError

    def finish(self):
        raise NotImplementedError


class Drawer:

    MAX_KEY_LENGTH = 10
    MAX_LIST_LENGTH = 100
    MAX_ITEMS = 100

    def __init__(self, drawer=None):
        self._compartments = list()
        if drawer != None:
            for compartment in drawer.compartments:
                self.add_compartment(compartment[0], compartment[1])

    @property
    def compartments(self):
        return self._compartments

    def add_compartment(self, key, value):
        if len(self._compartments) == Drawer.MAX_ITEMS:
            return
        if type(key) != str or len(key) > Drawer.MAX_KEY_LENGTH:
            raise ValueError(f'The key must be of type str and with a lenght shorter than {Drawer.MAX_KEY_LENGTH}')
        if type(value) not in [int, float, list]:
            raise AttributeError('The value must be of type int, float or list')
        if type(value) == list:
            if len(value) > Drawer.MAX_LIST_LENGTH:
                raise ValueError(f'Compartment list max value is {Drawer.MAX_LIST_LENGTH}')
            for item in value:
                if type(item) not in [int, float]:
                    raise AttributeError('List elements must be of type int or float')
        self._compartments.append((key, value))


class WordCount(Kernel):
    def setup(self):
        self.wordcount = dict()

    def add_word_occurrence(self, word):
        if word in self.wordcount:
            self.wordcount[word] += 1
            return
        self.wordcount[word] = 1

    def transform(self, value):
        tweet = value['body']
        for word in tweet.split():
            if len(word) <= Drawer.MAX_KEY_LENGTH:
                self.add_word_occurrence(word)

    def finish(self):
        drawer = Drawer()
        sorted_wordcount = sorted(((v, k) for k, v in self.wordcount.items()), reverse=True)

        compartment_counter = 0
        for value, key in sorted_wordcount:
            if compartment_counter == 100:
                break
            drawer.add_compartment(key, value)
            compartment_counter += 1
        return drawer


if __name__ == '__main__':
    import json
    with open('28A/tweets_debate.json', 'r') as input_file:
        tweets = json.load(input_file)

    kernel = WordCount()
    for tweet in tweets:
        kernel.transform(tweet)

    drawer = kernel.finish()
    for key, value in drawer.compartments:
        print(key, value)

import re

import os


class Twitter:
    version = '1.0'

    def __init__(self, backend=None):
        self.backend = backend
        self._tweets = []

    @property
    def tweets(self):
        if self.backend and not self._tweets:
            self._tweets = [line.rstrip('\n') for line in self.backend.readlines()]
        return self._tweets

    def tweet(self, message):
        if len(message) > 160:
            raise Exception('The message is too long')
        self.tweets.append(message)
        if self.backend:
            self.backend.write('\n'.join(self.tweets))

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall(r'#(\w+)', message)]

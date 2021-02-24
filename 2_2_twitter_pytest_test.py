import pytest

from twitter import Twitter


def test_twitter_initialization():
    twitter = Twitter()
    assert twitter


def test_tweet_single_message():
    twitter = Twitter()
    twitter.tweet('Test message')
    assert twitter.tweets == ['Test message']


def test_tweet_long_message():
    twitter = Twitter()
    with pytest.raises(Exception):
        twitter.tweet('test' * 41)
    assert twitter.tweets == []


@pytest.mark.parametrize('message, expected', (
        ('Test #first message', ['first']),
        ('#first message Test', ['first']),
        ('#FIRST message Test', ['first']),
        ('message Test #FIRST', ['first']),
        ('message Test #FIRST #second', ['first', 'second'])
))
def test_tweet_with_hashtag(message, expected):
    twitter = Twitter()
    assert twitter.find_hashtags(message) == expected

#  This code is replaced by this one above.
# def test_tweet_with_hashtag():
#     twitter = Twitter()
#     message = 'Test #first message'
#     assert 'first' in twitter.find_hashtags(message)
#
#
# def test_tweet_with_hashtag_on_the_beginning():
#     twitter = Twitter()
#     message = '#first message Test'
#     assert 'first' in twitter.find_hashtags(message)
#
#
# def test_tweet_with_hashtag_uppercase():
#     twitter = Twitter()
#     message = '#FIRST message Test'
#     assert 'FIRST' in twitter.find_hashtags(message)

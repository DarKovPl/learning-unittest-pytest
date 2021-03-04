import pytest

from twitter_26 import Twitter


@pytest.fixture()
def backend(tmpdir):
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)
    return twitter


def test_twitter_initialization(twitter):
    assert twitter


def test_tweet_single_message(twitter):
    twitter.tweet('Test message')
    assert twitter.tweets_messages == ['Test message']


def test_tweet_long_message(twitter):
    with pytest.raises(Exception):
        twitter.tweet('test' * 41)
    assert twitter.tweets_messages == []


def test_initialization_two_twitter_classes(backend):
    # Given
    twitter_1 = Twitter(backend=backend)
    twitter_2 = Twitter(backend=backend)

    # When
    twitter_1.tweet('Test 1')
    twitter_1.tweet('Test 2')

    # Then
    assert twitter_2.tweets_messages == ['Test 1', 'Test 2']


@pytest.mark.parametrize('message, expected', (
        ('Test #first message', ['first']),
        ('#first message Test', ['first']),
        ('#FIRST message Test', ['first']),
        ('message Test #FIRST', ['first']),
        ('message Test #FIRST #second', ['first', 'second'])
))
def test_tweet_with_hashtag(twitter, message, expected):
    assert twitter.find_hashtags(message) == expected

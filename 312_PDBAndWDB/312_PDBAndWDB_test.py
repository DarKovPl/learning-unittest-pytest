from unittest.mock import patch, Mock, MagicMock
import requests
import pytest

from twitter_312 import Twitter


class ResponseGetMock:
    def json(self):
        return {'avatar_url': 'test_mock_response'}


@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)
    return twitter


def test_twitter_initialization(twitter):
    assert twitter


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_single_message(avatar_mock, twitter):
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


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_username(avatar_mock, twitter):
    if not twitter.username:
        pytest.skip()

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message',
                               'key_from_twitter_class': 'test_mock_response',
                               'hashtags': []
                               }]
    avatar_mock.assert_called()


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hashtag_mock(avatar_mock, twitter):
    twitter.find_hashtags = Mock()
    twitter.find_hashtags.return_value = ['First']
    twitter.tweet('Test #second')
    assert twitter.tweets[0]['hashtags'] == ['First']
    twitter.find_hashtags.assert_called_with('Test #second')


def test_twitter_version(twitter):
    twitter.version = MagicMock()
    twitter.version.__eq__.return_value = '2.0'
    assert twitter.version == '2.0'


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_get_all_hashtags(avatar_mock, twitter):
    twitter.tweet('Test #first')
    twitter.tweet('Test #first #second')
    twitter.tweet('Test #third')
    assert twitter.get_all_hashtags() == {'first', 'second', 'third'}


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_get_all_hashtags_not_found(avatar_mock, twitter):
    twitter.tweet('Test first')
    assert twitter.get_all_hashtags() == "No hashtags found"

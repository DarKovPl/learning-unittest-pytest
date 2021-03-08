## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Code Examples](#code-examples)
## General Info
***
This repository shows the progress of learning the unit tests in Python using pytest.
## Screenshot
![Image text](https://res.cloudinary.com/practicaldev/image/fetch/s---dy84CM3--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/i/ls1nn7bpt6xfxtm6vbam.png)
## Technologies
***
A list of technologies used within the project:
* [Python](https://www.python.org/downloads/release/python-392/): Version 3.9.2
* [pytest](https://docs.pytest.org/en/stable/index.html): Version 6.2.2
## Code Examples
***
Link to file: https://github.com/DarKowPl/learning-unittest-pytest/blob/main/312_PDBAndWDB/312_PDBAndWDB_test.py

Examples of code:

~~~python
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
~~~

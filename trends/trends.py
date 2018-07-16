from .scrap import Content
from .models import Post
import newspaper
import nltk
from collections import Counter

class Analytics():
    def __init__(self):
        self._scrapper = Content()

    def hot_topics(self):
        hot_topics = newspaper.hot()
        hot_topics_str = []
        for topic in hot_topics:
            split_topic = topic.lower().split()
            hot_topics_str.extend(split_topic)
        recent_topics = self._scrapper.get_recent_topics(7)
        hot_count = self._scrapper.get_hot_count(hot_topics_str, recent_topics)
        return hot_count

    def hot_authors(self):
        return None

    def hot_websites(self):
        hot_topics = newspaper.hot()
        hot_topics_str = []
        for topic in hot_topics:
            split_topic = topic.lower().split()
            hot_topics_str.extend(split_topic)
        hot_count = self._scrapper.get_web_count(hot_topics_str, 7)
        return hot_count

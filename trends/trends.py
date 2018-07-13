from .scrap import Content
from .models import Post
import newspaper
import nltk
from collections import Counter

class Analytics():
    def __init__(self):
        self._scrapper = Content()

    def hot_topics(self):
        recent_post_tuples = self._scrapper.get_articles_range(7)
        hot_topics = newspaper.hot()
        hot_topics_str = []
        for topic in hot_topics:
            split_topic = topic.lower().split()
            hot_topics_str.extend(split_topic)
        print("curr hot", hot_topics_str)
        common_topics_total = []
        print("len tuples", len(recent_post_tuples))

        total_topics = []
        for post_tuple in recent_post_tuples:
            tuple_topics = self._scrapper.get_topics(post_tuple)[1:-1]
            print('tuple_topics', type(tuple_topics))
            for topic in tuple_topics:
                total_topics.append(topic)
        common_topics = set(total_topics) & set(hot_topics_str)
        print('common_topics', common_topics)

        return common_topics

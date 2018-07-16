import newspaper
from newspaper import Article
from .models import Post, Posts, Topic
import time
from datetime import datetime
from datetime import timedelta
import pytz

class ScrapException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = "URL not provided"

class Content():
    def __init__(self):
        self._sites = []
        self._sites.append('http://www.cnn.com')
        print('sites', self._sites)
        self._sites.append('http://www.foxnews.com')
        self._sites.append('http://www.huffingtonpost.com')
        self._sites.append('https://www.buzzfeed.com/news')
        self._sites.append('https://www.usatoday.com/')
        self._sites.append('https://www.reuters.com/news/us')
        self._sites.append('https://www.nytimes.com/')
        self._sites.append('https://www.npr.org/')

    def add_article(self, article, paper):
        try:
            article.download()
            article.parse()
            article.nlp()
            utc_date = article.publish_date.astimezone(pytz.timezone('UTC'))
            post = Posts(article=article.title,
                         author= article.authors,
                         website=paper,
                         published=utc_date)
            post.save()
            topics = article.keywords
            for topic in topics:
                topic_entry = Topic(post=post,
                                    topic=topic,
                                    published=utc_date)
                topic_entry.save()
        except Exception as e:
            print("Article", article.title, "Exception", str(e))
            return False
        return True

    def add_paper(self, site, cached=True):
        print('[DEBUG 43 scrap]: paper site', site)
        curr_sites = list(Posts.objects.values_list('website').distinct())
        if site not in curr_sites:
            cached = False
        paper = newspaper.build(site, language='en') #, memoize_articles=cached)
        print("[DEBUG 45 scrap]: paper.articles len = ", len(paper.articles))
        succ = 0
        counter = 0
        for article in paper.articles:
            tmp_succ = self.add_article(article, paper.brand)
            counter += 1
            print("[DEBUG 51 scrap]: tmp_succ for article #", counter)
            if tmp_succ:
                succ += 1

        diff = len(paper.articles) - succ
        if diff == 0:
            print("All articles succesfully added")
        else:
            print(diff, "articles unsucessfully added")

    def get_recent_topics(self, diff_days):
        curr = datetime.now()
        diff = timedelta(diff_days)
        lower_bound = curr.date() - diff
        return Topic.objects.filter(published__gte = lower_bound)

    def get_recent_post(self, diff_days, paper):
        curr = datetime.now()
        diff = timedelta(diff_days)
        lower_bound = curr.date() - diff
        return Posts.objects.filter(published__gte = lower_bound, website=paper)

    def get_web_count(self, hot_topics, diff_days):
        matchedDict = {}
        recent_topics = self.get_recent_topics(diff_days)
        sites = Posts.objects.values_list('website' ,flat=True).distinct()
        print("[DEBUG 87 scrap]: sites", sites)
        for site in sites:
            qset = self.get_recent_post(diff_days, site)
            total = 0
            if qset.count() > 0:
                for post in qset:
                    matched = False
                    post_topics = post.topic_set.all()
                    matched_topics = self.get_hot_count(hot_topics, post_topics)
                    print("[DEBUG 96 scrap]: curr_site", site, "matched_topics", matched_topics)
                    values = matched_topics.values()
                    for value in values:
                        if value > 0:
                            matched = True
                    total += (1 if matched else 0)
            matchedDict[site] = total
            print("[DEBUG 103 scrap]: site", site, "total", total)
        return matchedDict

    def get_hot_count(self, hot_topics, recent_topics):
        matchedDict = {}
#        recent_topics = self.get_recent_topics(diff_days)
        for topic in hot_topics:
            qset = recent_topics.filter(topic=topic)
            if qset.count() > 0:
                matchedDict[topic] = qset.count()
        return matchedDict

    def get_articles_range(self, diff_days):
        curr = datetime.now()
        diff = timedelta(diff_days)
        lower_bound = curr.date() - diff

        websites = Post.objects.values_list('website', flat=True).distinct()
        article_tuples = []
        for site in websites:
            site_articles = Post.objects.filter(published__gte= lower_bound, website=site)
            print(site + str(site_articles.count()))
            for article in site_articles:
                tuple = self.get_article_tuple(article)
                article_tuples.append(tuple)
        return article_tuples

    def get_article_tuple(self, article):
        return (article.article,
                article.author,
                article.website,
                article.published,
                article.topics)

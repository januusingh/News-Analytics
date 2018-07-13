import newspaper
from newspaper import Article
from .models import Post
import time
from datetime import datetime
from datetime import timedelta

class ScrapException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = "URL not provided"

class Content():
    def __init__(self):
        self._sites = []
        self._sites.append('http://www.cnn.com')
        print('sites', self._sites)
#        self._sites.append('http://www.foxnews.com')
#        self._sites.append('http://www.huffingtonpost.com')
#        self._sites.append('https://www.buzzfeed.com/news')
#        self._sites.append('https://www.usatoday.com/')

    def add_article(self, article, paper):
        try:
            article.download()
            article.parse()
            article.nlp()
            post = Posts(article=article.title,
                         author= article.authors,
                         website=paper,
                         published=art.publish_date)
            post.save()
            topics = art.keywords
            for topic in topics:
                topic_entry = Topic(post=post, topic=topic)
                topic_entry.save()
        except:
            return False
        return True

    def add_paper(self, site, cached=True):
        print('paper site', site)
        paper = newspaper.build(site, language='en', memoize_articles=cached)
        succ = 0
        for article in paper.articles:
            tmp_succ = self.add_article(article, paper.brand)
            if tmp_succ:
                suc += 1

        diff = len(paper.articles) - succ
        if diff == 0:
            print("All articles succesfully added")
        else:
            print(diff, "articles unsucessfully added")

    def get_articles_range(self, diff_days):
        try:
            self.articles()
        except:
            pass
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

    def get_topics(self, tuple):
        return tuple[4]

    def data(self, url):
        paper = newspaper.build(url, language='en')
        for article in paper.articles:
            try:
                article.download()
                article.parse()
                #time.sleep(1)
                article.nlp()
                post = Post(article     = article.title,
                            author      = (article.authors if article.authors else []),
                            website     = paper.brand,
                            published   = article.publish_date,
                            topics      = (article.keywords if article.keywords else []))
                post.save()
            except:
                pass

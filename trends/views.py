from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .scrap import Content
from .models import Post, Posts
from .trends import Analytics
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta

# Create your views here.

def index(request):
	return HttpResponse('Hello World!')

def current_articles(request):
	articles = Post.objects.all()
	articles_str = [str(article) for article in articles]
	response = ", \n".join(articles_str)
	return JsonResponse(response, safe=False)

def scrap_test(request):
	scrapper = Content()
	sites = scrapper._sites
	for site in sites:
		articles = scrapper.add_paper(site)
	response = Posts.objects.all().count()
	return HttpResponse(response)

def home(request):
	response = "This is an index"
	return JsonResponse(response, safe=False)

def hot_topic_view(request):
	anal = Analytics()
	topics = anal.hot_websites()
	response = ""
	if topics is None:
		response = "Nothing"
	else:
		response = str(topics)
	return HttpResponse(response)

class HomeView(View):
	def get(self, request):
		return render(request, 'charts.html', {})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
		#Get articles within past 7 days
        curr = datetime.now()
        diff = timedelta(7)
        lower_bound = curr.date() - diff
        websites = Post.objects.values_list('website', flat=True).distinct()
        dict = {}
        for site in websites:
            site_articles = Post.objects.filter(published__gte= lower_bound, website=site)
            count = site_articles.count()
            dict[site] = count

		#Trends
        analytics = Analytics()
        hot = analytics.hot_topics()
        hot_web = analytics.hot_websites()
        data = {
#		    "labels" : dict.keys(),
#		    "count" : dict.values()
            "labels" : hot.keys(),
            "count" : hot.values(),
			"labels2" : hot_web.keys(),
			"count2" : hot_web.values(),}
        return Response(data)

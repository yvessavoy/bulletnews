from django.views.generic.list import ListView
from django.shortcuts import render

from . import models


class Index(ListView):
    model = models.Article
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['origins'] = models.Article.ORIGINS
        return context


def news_by_origin(req, origin):
    articles = models.Article.objects.filter(origin=origin)
    return render(req, 'web/index.html', {
        'object_list': articles,
        'origins': models.Article.ORIGINS
    })
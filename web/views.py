from django.views.generic.list import ListView
from django.shortcuts import render

from . import models


class Index(ListView):
    model = models.Article
    template_name = 'web/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['origins'] = models.Article.ORIGINS
        return context

    def get_queryset(self):
        if 'origin' in self.kwargs:
            return models.Article.objects.filter(origin=self.kwargs['origin']).order_by('-publish_tsd')
        else:
            return models.Article.objects.all().order_by('-publish_tsd')
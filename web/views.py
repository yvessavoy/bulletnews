from django.views.generic.list import ListView

from . import models


class Index(ListView):
    model = models.Article
    template_name = 'web/index.html'

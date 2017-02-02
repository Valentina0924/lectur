from django.shortcuts import render

import datetime;
from django.views.generic import View, FormView, UpdateView, CreateView, DetailView, ListView, TemplateView;
from django.http import HttpResponseRedirect, HttpResponse;
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# from models import

# Create your views here.

class Home(TemplateView):
    """docstring for Home."""
    template_name="val.html"
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["usuarios"]=User.objects.all();
        context["estado"]= 5;
        return context

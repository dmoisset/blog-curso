from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, FormView, TemplateView
from django.utils.decorators import method_decorator




class Index(TemplateView):
    template_name = 'cafeblog/index.html'
index = Index.as_view()

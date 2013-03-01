from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, FormView, TemplateView
from django.utils.decorators import method_decorator
from forms import ProfileForm
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from models import UserProfile



class Index(TemplateView):
    template_name = 'cafeblog/index.html'
index = Index.as_view()

@login_required
def profile(request):
    try:
        user_profile = request.user.get_profile()
        return render_to_response('cafeblog/profile.html',
                                  {'user_profile': user_profile, },
                                  context_instance=RequestContext(request),)
    except ObjectDoesNotExist:
        redirect('cafeblog:profile_edit')

@login_required
def profile_edit(request):
    try:
        user_profile = request.user.get_profile()
    except ObjectDoesNotExist:
        user_profile = UserProfile(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile, label_suffix='')
        if profile_form.is_valid():
            profile_form.save()
            return redirect('cafeblog:profile')
    elif request.method == 'GET':
        profile_form = ProfileForm(instance=user_profile, label_suffix='')
    return render_to_response('cafeblog/profile_edit.html',
                  {'profile_form': profile_form, },
                  context_instance=RequestContext(request))

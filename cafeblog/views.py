from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from cafeblog.forms import SignUpForm


class Index(TemplateView):
    template_name = 'cafeblog/index.html'
index = Index.as_view()


class SignUp(FormView):
    form_class = SignUpForm
    template_name = 'cafeblog/signup.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('cafeblog:index')
signup = SignUp.as_view()

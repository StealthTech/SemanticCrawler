from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

from .forms import SignInForm

from utils.http import WebStatus


class GenericPageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(GenericPageView, self).get_context_data(**kwargs)
        context['login_form'] = SignInForm()
        return context


class AjaxResponseMixin(object):
    def __init__(self):
        self.response = {}
        self.status = WebStatus.http.internal_server_error

    @property
    def ajax_response(self):
        return JsonResponse(self.response, status=self.status)


class LandingView(GenericPageView):
    template_name = 'pages/index.html'

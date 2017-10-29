from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse

from pages.forms import SignInForm, SignUpForm

from utils.http import WebStatus


class AjaxResponseMixin(object):
    def __init__(self):
        self.response = {}
        self.status = WebStatus.http.internal_server_error

    @property
    def ajax_response(self):
        return JsonResponse(self.response, status=self.status)


class LoginView(AjaxResponseMixin, View):
    def post(self, request, *args, **kwargs):
        r = self.request
        if r.is_ajax():
            if not r.user.is_authenticated():
                form = SignInForm(data=r.POST)
                if form.is_valid():
                    email = r.POST['username']
                    password = r.POST['password']
                    user = authenticate(r, email=email, password=password)

                    if user:
                        login(r, user)
                        self.response['status'] = WebStatus.json.success
                        self.response['message'] = 'Запрос принят.'
                        self.status = WebStatus.http.success
                    else:
                        self.response['status'] = WebStatus.json.fail
                        self.response['message'] = 'Запрос отклонён. Произошла ошибка аутентификации.'
                        self.status = WebStatus.http.bad_request
                else:
                    self.response['status'] = WebStatus.json.fail
                    self.response['message'] = 'Запрос отклонён. Данные формы содержат ошибки.'
                    self.response['errors'] = form.errors
                    self.status = WebStatus.http.bad_request
            else:
                self.response['status'] = WebStatus.json.fail
                self.response['message'] = 'Запрос отклонён. Пользователь уже авторизован.'
                self.status = WebStatus.http.forbidden

            return self.ajax_response
        else:
            raise Http404


class LogoutView(AjaxResponseMixin, View):
    def get(self, request, *args, **kwargs):
        r = self.request
        if r.is_ajax():

            if r.user.is_authenticated():
                logout(r)
                self.response['status'] = WebStatus.json.success
                self.response['message'] = 'Запрос принят.'
                self.status = WebStatus.http.success
            else:
                self.response['status'] = WebStatus.json.fail
                self.response['message'] = 'Запрос отклонён. Пользователь не авторизован.'
                self.status = WebStatus.http.forbidden

            return self.ajax_response
        else:
            logout(r)
            return redirect('pages:index')

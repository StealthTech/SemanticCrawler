from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import Http404

from pages.views import AjaxResponseMixin
from pages.forms import SignInForm

from utils.http import WebStatus


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

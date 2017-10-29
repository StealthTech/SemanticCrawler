from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from .forms import SignInForm, SignUpForm, ProfileEditForm, LaunchForm
from core.views import AjaxResponseMixin
from core.models import User
from scanner.models import ScanRequest

from utils.http import WebStatus


class GenericPageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(GenericPageView, self).get_context_data(**kwargs)
        context['login_form'] = SignInForm()
        return context


class LandingView(GenericPageView):
    template_name = 'pages/index.html'


class PanelView(GenericPageView):
    template_name = 'pages/panel.html'

    def get_context_data(self, **kwargs):
        context = super(PanelView, self).get_context_data(**kwargs)

        scan_list = []
        if self.request.user.is_authenticated():
            scan_list = ScanRequest.objects.filter(user=self.request.user)
        context['scan_list'] = scan_list
        return context


class LaunchView(AjaxResponseMixin, GenericPageView):
    template_name = 'pages/launch.html'

    def get_context_data(self, **kwargs):
        context = super(LaunchView, self).get_context_data(**kwargs)
        context['launch_form'] = LaunchForm()
        return context

    def post(self, request, *args, **kwargs):
        r = self.request
        if not r.is_ajax():
            return redirect('pages:index')

        if r.user.is_authenticated():

            form = LaunchForm(r.POST)

            if form.is_valid():
                scan_request = form.save(commit=False)
                scan_request.user = self.request.user
                scan_request.save()

                self.response['status'] = WebStatus.json.success
                self.response['message'] = 'Запрос принят.'
                self.response['target_url'] = reverse('pages:index')
                self.status = WebStatus.http.success
            else:
                self.response['status'] = WebStatus.json.fail
                self.response['message'] = 'Запрос отклонён. Данные формы содержат ошибки.'
                self.response['errors'] = form.errors
                self.status = WebStatus.http.bad_request
        else:
            self.response['status'] = WebStatus.json.fail
            self.response['message'] = 'Запрос отклонён. Пользователь не авторизован.'
            self.status = WebStatus.http.forbidden

        return self.ajax_response


class SignUpView(AjaxResponseMixin, GenericPageView):
    template_name = 'pages/signup.html'

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['signup_form'] = SignUpForm()
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('pages:index', nickname=self.request.user.nickname)
        else:
            return super(SignUpView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        r = self.request
        if not r.is_ajax():
            return redirect('pages:index')

        if not r.user.is_authenticated():

            form = SignUpForm(r.POST)

            if form.is_valid():
                user = form.save()
                user.email_verified = False

                # if EMAIL_ENABLED:
                #     email = AccountActivationEmail(r, user)
                #     email.send()

                user.save()
                login(r, user)

                self.response['status'] = WebStatus.json.success
                self.response['message'] = 'Запрос принят.'
                self.response['target_url'] = reverse('pages:index')
                self.status = WebStatus.http.success
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


class ProfileView(AjaxResponseMixin, GenericPageView):
    template_name = 'pages/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        u = get_object_or_404(User, nickname=self.kwargs['nickname'])

        context['profile'] = u
        if self.request.user.pk == u.pk:
            context['is_owner'] = True
            context['profile_edit_form'] = ProfileEditForm(instance=u)
        else:
            context['is_owner'] = False

        return context

    def post(self, request, *args, **kwargs):
        r = self.request
        if not r.is_ajax():
            return redirect('pages:index')

        if request.user.is_authenticated():
            instance = get_object_or_404(User, nickname=request.user.nickname)

            if instance.pk == request.user.pk:
                form = ProfileEditForm(request.POST or None, request.FILES or None, instance=instance)
                if form.is_valid():
                    form.save()
                    self.response['status'] = WebStatus.json.success
                    self.response['message'] = 'Запрос принят.'
                    self.response['target_url'] = reverse('pages:profile', kwargs={'nickname': instance.nickname})
                    self.status = WebStatus.http.success
                else:
                    self.response['status'] = WebStatus.json.fail
                    self.response['message'] = 'Запрос отклонён. Данные формы содержат ошибки.'
                    self.response['errors'] = form.errors
                    self.status = WebStatus.http.bad_request
            else:
                self.response['status'] = WebStatus.json.fail
                self.response['message'] = 'Запрос отклонён. Пользователь не является владельцем профиля.'
                self.status = WebStatus.http.forbidden
        else:
            self.response['status'] = WebStatus.json.fail
            self.response['message'] = 'Запрос отклонён. Пользователь не авторизован.'
            self.status = WebStatus.http.forbidden

        return self.ajax_response

from django.shortcuts import render
from django.views import generic
from accounts.forms import TestForm

from accounts.models import Account
from app.services.Core import Core

class AccountView(generic.View):
    model = Account
    template_name = 'accounts/index.html'

    def get(self, request, *args, **kwargs):
        form = TestForm(request.POST, request.GET, request.FILES)

        print(Core.request.session.session_key, request.session.session_key)

        return render(request, self.template_name, { 'form': form })

    def post(self, request, *args, **kwargs):
        form = TestForm(request.POST, request.GET, request.FILES)

        if form.is_valid():
            print('cleaned_data => ', form.cleaned_data)

        return render(request, self.template_name, { 'form': form })

from django.http import JsonResponse
from django.views.generic.edit import FormView

from accounts.forms import TestForm


class EditFormView(FormView):
    form_class = TestForm
    success_url = '/thanks/'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Call ajax
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

from django.urls import include, path

from accounts.views import AccountView

app_name = "accounts"
urlpatterns = [
    path('', AccountView.as_view(), name='index')
]

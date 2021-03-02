from django.urls import path
from .views import sign_up_for_newsletter

app_name = "users"
urlpatterns = [
  path('newsletter', sign_up_for_newsletter)
]

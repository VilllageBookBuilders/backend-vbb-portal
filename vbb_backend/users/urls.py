from django.urls import path
from .views import NewsletterSignup

app_name = "users"
urlpatterns = [
  path('newsletter/', NewsletterSignup.as_view())
]

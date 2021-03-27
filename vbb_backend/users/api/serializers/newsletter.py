from rest_framework import serializers

from vbb_backend.users.models import NewsletterSubscriber


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        exclude = ("deleted", "id", "external_id")

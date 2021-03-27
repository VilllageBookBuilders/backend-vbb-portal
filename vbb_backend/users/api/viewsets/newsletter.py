from rest_framework import request
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import PermissionDenied
from vbb_backend.users.api.serializers.newsletter import NewsletterSubscriberSerializer
from vbb_backend.users.models import NewsletterSubscriber


class NewsletterSubscriberViewSet(
    CreateModelMixin, ListModelMixin, RetrieveAPIView, GenericViewSet
):
    queryset = NewsletterSubscriber.objects.all()
    permission_classes = []
    serializer_class = NewsletterSubscriberSerializer

    def get_queryset(self):
        if self.action in ["list", "retrieve"] and not self.request.user.is_superuser:
            raise PermissionDenied("Not Authorised to view this endpoint")
        return super().get_queryset()
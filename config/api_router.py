from django.conf import settings
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from vbb_backend.program.api.viewsets.classroom import ClassroomViewSet
from vbb_backend.program.api.viewsets.computer import ComputerViewSet
from vbb_backend.program.api.viewsets.program import ProgramViewSet
from vbb_backend.program.api.viewsets.school import SchoolViewSet
from vbb_backend.program.api.viewsets.slot import SlotViewSet
from vbb_backend.program.api.viewsets.slotStudent import StudentSlotViewSet
from vbb_backend.users.api.viewsets.student import StudentViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("program", ProgramViewSet)

program_nested_router = NestedSimpleRouter(router, r"program", lookup="program")


program_nested_router.register(r"school", SchoolViewSet)

program_nested_router.register(r"computer", ComputerViewSet)

computer_nested_router = NestedSimpleRouter(
    program_nested_router, r"computer", lookup="computer"
)

computer_nested_router.register(r"slot", SlotViewSet)


slot_nested_router = NestedSimpleRouter(computer_nested_router, r"slot", lookup="slot")

slot_nested_router.register(r"student", StudentSlotViewSet)


school_nested_router = NestedSimpleRouter(
    program_nested_router, r"school", lookup="school"
)

school_nested_router.register(r"classroom", ClassroomViewSet)

school_nested_router.register(r"student", StudentViewSet)


classroom_nested_router = NestedSimpleRouter(
    school_nested_router, r"classroom", lookup="classroom"
)

app_name = "api"

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^", include(program_nested_router.urls)),
    url(r"^", include(school_nested_router.urls)),
    url(r"^", include(classroom_nested_router.urls)),
    url(r"^", include(computer_nested_router.urls)),
    url(r"^", include(slot_nested_router.urls)),
]

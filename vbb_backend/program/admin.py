from django.contrib import admin

from vbb_backend.program.models import Program, School, Computer, Slot

admin.site.register(Program)
admin.site.register(Computer)
admin.site.register(Slot)
admin.site.register(School)

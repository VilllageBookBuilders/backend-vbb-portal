from django.contrib import admin


from vbb_backend.users.models import User, Mentor, Student, HeadMaster
from django.contrib.auth.admin import UserAdmin


# class MyUserAdmin(UserAdmin):
#     model = User

#     fieldsets = UserAdmin.fieldsets + (
#         (None, {"fields": ("user_type", "external_id")}),
#     )


# admin.site.register(User, MyUserAdmin)

admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(HeadMaster)
from django.contrib import admin
from  django.contrib.auth.models  import  Group  # new
from django.contrib.auth.admin import UserAdmin

from .models import *


class CustomAdmin(UserAdmin):

    list_filter = (["is_superuser"])
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('email',)}),
        # (('Permissions'), {
        #     'fields': [],#'is_active', 'is_staff', 'is_superuser', 'groups'
        # }),
        # (('Important dates'), {'fields': []}), #'last_login', 'date_joined'
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', ),
        }),
    )


admin.site.site_header = 'Cybersecurity Gamification - Administration'

admin.site.register(player)
admin.site.register(teamscore)
admin.site.register(game)
admin.site.register(question)

admin.site.register(module)
admin.site.register(module_segment)
admin.site.register(module_question)

admin.site.register(credit)
admin.site.register(User, CustomAdmin)

admin.site.unregister(Group)

@admin.register(team)
class TeamAdmin(admin.ModelAdmin):
      exclude = ('questions','module_questions')


@admin.register(module_game)
class ModuleGameAdmin(admin.ModelAdmin):
      exclude = ('score',)
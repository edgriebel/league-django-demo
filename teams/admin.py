from django.contrib import admin
from teams import models


class TeamInline(admin.TabularInline):
    model = models.Team
    readonly_fields = (
        "id",
        "name",
        "abbr",
    )


class TeamAdmin(admin.ModelAdmin):
    model = models.Team


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    model = models.League
    inlines = [TeamInline]
    list_select_related = True


# admin.site.register(models.League)
admin.site.register(models.Team)

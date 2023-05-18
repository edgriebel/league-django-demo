from django.shortcuts import render
from django.http import HttpResponse
from teams.models import League, Team


def index(request) -> HttpResponse:
    leagues = sorted(League.objects.all(), key=lambda l: l.abbr)
    teams = sorted(Team.objects.all(), key=lambda t: t.league.abbr)
    print(f"Leagues: {leagues}")
    context = {"leagues": leagues, "teams": teams}
    return render(request, "leagues.html", context)


def detail(request, league_id: int) -> HttpResponse:
    teams = Team.objects.filter(league=league_id)
    league = League.objects.get(id=league_id)
    context = {"teams": teams, "league": league}
    return render(request, "teams.html", context)

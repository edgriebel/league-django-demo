from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from teams import models
import argparse
import csv

LEAGUE_FILE = "leagues.csv"
TEAM_FILE = "teams.csv"


class Command(BaseCommand):
    help = "Loads leagues.csv and teams.csv to db"
    requires_migrations_checks = True

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-d",
            "--dir",
            nargs=1,
            type=str,
            help="Specify the directory files are located",
        )
        parser.add_argument(
            "--db",
            action=argparse.BooleanOptionalAction,
            help="Load data into database from CSV files",
        )
        parser.add_argument(
            "--users",
            action=argparse.BooleanOptionalAction,
            help="Create default users",
        )

    def handle(self, *args, **options):
        print(f"options: {options}")
        # If neither specified then do both
        if options.get("users") or not (options.get("db") or options.get("users")):
            self.create_users(args, options)
        if options.get("db") or not (options.get("db") or options.get("users")):
            self.load_data(args, options)

    def create_users(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Existing users: {User.objects.all()}"))

        if not User.objects.filter(username="admin"):
            self.stdout.write(self.style.SUCCESS("Creating user admin"))
            User.objects.create_superuser(
                username="admin",
                email=None,
                password="123123",
            )

        commish = User.objects.filter(username="commish")
        if commish:
            commish = commish[0]
        else:
            self.stdout.write(self.style.SUCCESS("Creating user commish"))
            commish = User.objects.create_user(
                username="commish",
                email=None,
                password="123123",
                is_staff=True,
            )

        # add permissions to commish
        league_content_type = ContentType.objects.get_for_model(models.League)
        for perm in ["change", "view"]:
            permission = Permission.objects.get(
                codename=f"{perm}_league", content_type=league_content_type
            )
            commish.user_permissions.add(permission)

        team_content_type = ContentType.objects.get_for_model(models.Team)
        for perm in ["add", "delete", "change", "view"]:
            permission = Permission.objects.get(
                codename=f"{perm}_team", content_type=team_content_type
            )
            commish.user_permissions.add(permission)

    def load_data(self, *args, **options):
        file_dir = (options.get("dir") or ["teams"])[0]
        self.stdout.write(self.style.SUCCESS(f"Reading files from {file_dir}"))

        with open(f"{file_dir}/{LEAGUE_FILE}", newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)
            leagues = [models.League(**dict(zip(headers, row))) for row in reader]
        self.stdout.write(self.style.SUCCESS(f"Leagues to load: {len(leagues)}"))
        leagues_dict = {l.abbr: l for l in leagues}

        with open(f"{file_dir}/{TEAM_FILE}", newline="") as f:
            teams = []
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                rec = dict(zip(headers, row))
                # if we don't find a match it's ok to raise an exception
                rec["league"] = leagues_dict[rec["league"]]
                teams.append(models.Team(**rec))
        self.stdout.write(self.style.SUCCESS(f"Teams to load: {len(teams)}"))

        # Now save to database
        leagues_db = models.League.objects.bulk_create(leagues)
        self.stdout.write(self.style.SUCCESS(f"Leagues loaded: {len(leagues_db)}"))
        teams_db = models.Team.objects.bulk_create(teams)
        self.stdout.write(self.style.SUCCESS(f"Teams loaded: {len(teams_db)}"))

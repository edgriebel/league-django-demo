from django.db import models

# Create your models here.


class League(models.Model):
    # ID auto-created and comes from file
    abbr = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __repr__(self):
        return f"id: {self.id} abbr: {self.abbr} name: {self.name}"

    def __str__(self):
        return self.name


class Team(models.Model):
    abbr = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.id}: abbr: {self.abbr} name: {self.name} league: {self.league}"

    def __str__(self):
        return self.name

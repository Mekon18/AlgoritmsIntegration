"""
Definition of models.
"""

from django.db import models

# Create your models here.
class Coordinate(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    #amountOfFood = models.FloatField()

class CoordinateObcts(models.Model):
    obtacleX = models.FloatField()
    obtacleY = models.FloatField()

class CoordinateAnts(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    #z = models.FloatField()

class FireflyPopulation(models.Model):
    num_worms = models.IntegerField()
    nturns = models.IntegerField()
    influence_factor = models.IntegerField()
    start = models.FloatField()
    end = models.FloatField()
    max_jitter = models.FloatField()
    function = models.TextField()


class FireflyAgent(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    agent_id = models.IntegerField()
    population_id = models.ForeignKey(FireflyPopulation, on_delete=models.CASCADE)

class FishesPopulation(models.Model):
    population_size = models.IntegerField()
    iteration_count = models.IntegerField()
    weight_max = models.FloatField()
    speed = models.FloatField()
    min_x = models.FloatField()
    max_x = models.FloatField()
    min_y = models.FloatField()
    max_y = models.FloatField()
    error = models.FloatField()
    function = models.IntegerField()

class FishAgent(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    agent_id = models.IntegerField()
    population_id = models.ForeignKey(FishesPopulation, on_delete=models.CASCADE)

class BeesPopulation(models.Model):
    population_size = models.IntegerField()
    iteration_count = models.IntegerField()
    funcName = models.TextField()

class BeeAgent(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    agent_id = models.IntegerField()
    population_id = models.ForeignKey(BeesPopulation, on_delete=models.CASCADE)


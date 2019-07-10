import random as r
from django.db import models
#from django.contrib.postgres.fields import ArrayField
from .model_ant import Ant
from .model_const import Const
import app.models as mod
#import aco.const as const

class Field(models.Model):
	class Meta:
		app_label='Field'
	#id = models.IntegerField(primary_key=True)
	matrix = []
	foodList = []
	foodAmounts = []
	ants = []
	def initField(self):
		self.const = Const()
		self.matrix.clear()
		self.foodList.clear()
		self.foodAmounts.clear()
		for i in range(100):
			self.matrix.append([])
			for j in range(100):
				self.matrix[i].append(self.const.initFeromone)
		self.matrix[self.const.spawnX][self.const.spawnY] = "spawn"

		for i in range(self.const.numFood):
			putFoodSuccess = False
			while not putFoodSuccess:
				foodX = r.randint(5, 94)
				foodY = r.randint(5, 94)
				mod.Coordinate.objects.create(x = foodX, y = foodY)
				foodXSuccess = (abs(foodX - self.const.spawnX) in range(self.const.minFoodDistance, self.const.maxFoodDistance)) and (abs(foodY - self.const.spawnY) in range(0, self.const.maxFoodDistance))
				foodYSuccess = (abs(foodY - self.const.spawnY) in range(self.const.minFoodDistance, self.const.maxFoodDistance)) and (abs(foodX - self.const.spawnX) in range(0, self.const.maxFoodDistance))
				if foodXSuccess or foodYSuccess:
					if [foodX, foodY] not in self.foodList:
						self.foodList.append([foodX, foodY])
						self.foodAmounts.append(self.const.initialFoodAmount)
						self.matrix[foodX][foodY] = "food"
						putFoodSuccess = True
					

		for i in range(self.const.numObstacles):
			putObstacleSuccess = 0
			while putObstacleSuccess < self.const.numFood + 1: #количество еды + точка спавна
				obstacleX = r.randint(0, 99)
				obstacleY = r.randint(0, 99)
				mod.CoordinateObcts.objects.create(obtacleX = obstacleX, obtacleY = obstacleY)
				if not ( (self.matrix[obstacleX][obstacleY] == "obstacle") and (self.matrix[obstacleX][obstacleY] == "food") and (self.matrix[obstacleX][obstacleY] == "spawn")): #OR
					spawnXSuccess = (obstacleX <= self.const.spawnX - self.const.freeSpace) or (obstacleX >= self.const.spawnX + self.const.freeSpace)
					spawnYSuccess = (obstacleY <= self.const.spawnY - self.const.freeSpace) or (obstacleY >= self.const.spawnY + self.const.freeSpace)
					if spawnXSuccess or spawnYSuccess:
						putObstacleSuccess += 1
					else:
						putObstacleSuccess = 0
						continue
					for i in range(self.const.numFood):
						foodX = self.foodList[i][0]
						foodY = self.foodList[i][1]
						foodXSuccess = (obstacleX <= foodX - self.const.freeSpace) or (obstacleX >= foodX + self.const.freeSpace)
						foodYSuccess = (obstacleY <= foodY - self.const.freeSpace) or (obstacleY >= foodY + self.const.freeSpace)
						if foodXSuccess or foodYSuccess:
							putObstacleSuccess += 1
						else:
							putObstacleSuccess = 0
							continue
			self.matrix[obstacleX][obstacleY] = "obstacle"

	# инициализация муравьёв
	def createAnts(self):
		self.ants.clear()
		numLeet = int(self.const.leetQ / 100 * self.const.numAnts) # кол-во элитных муравьев
		for i in range(self.const.numAnts):
			ant = Ant(id = i)
			self.ants.append(ant)
			if (numLeet > 0):
				ant.leet = True
				numLeet -= 1
			#ant.save()
	
	def saveAnts(self):
		for i in range(self.const.numAnts):
			self.ants[i].save()


	def recoverAnts(self):
		for i in range(self.const.numAnts):
			ant = Ant.objects.get(id = i)
			self.ants.append(ant)

	def moveAnts(self):
		for ant in self.ants:
			ant.turn(self)

	# глобальное испарение феромона
	def globalEvaporate(self):
		for i in range(100):
			for j in range(100):
				if type(self.matrix[i][j]) == type(0.0):	
					self.matrix[i][j] *= (1 - self.const.gp);

	def noFood(self):
		if self.const.initialFoodAmount > 0:
			for i in self.foodAmounts:
				if i > 0:
					return False
			return True
		else:
			return False

# Create your models here.

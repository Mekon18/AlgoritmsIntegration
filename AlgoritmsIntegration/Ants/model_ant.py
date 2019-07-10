from django.db import models
import random as r
#from django.contrib.postgres.fields import ArrayField
import Ants.const as const

class Ant(models.Model):
	class Meta:
		app_label='Ant'
	id = models.IntegerField(primary_key=True)
	x = models.IntegerField(default = 50)
	y = models.IntegerField(default = 50)
	tabooList = []
	tabooListIndex = models.IntegerField(default=0)
	putFeromone = models.BooleanField(default=False)
	l0 = models.IntegerField(default = 0)
	leet = models.BooleanField(default=False) #delete default
	#newDir = 0

	def move(self, dir):
		if [self.x, self.y] not in self.tabooList:
			self.tabooList.append([self.x, self.y])
		dx, dy = 0, 0
			
		if dir == 0:
			dy = -1
		if dir == 1:
			dy = -1
			dx = 1
		if dir == 2:
			dx = 1
		if dir == 3:
			dx = 1
			dy = 1
		if dir == 4:
			dy = 1
		if dir == 5:
			dy = 1
			dx = -1
		if dir == 6:
			dx = -1
		if dir == 7:
			dx = -1
			dy = -1

		self.x += dx
		self.y += dy
		
		if [self.x, self.y] not in self.tabooList:
			self.tabooList.append([self.x, self.y])

		if (dx * dy == 0):
			self.l0 += 1
		else:
			self.l0 += 2 ** .5

	def tryMove(self, dir):
		if dir == 0:
			return [self.x, self.y - 1]
		if dir == 1:
			return [self.x + 1, self.y - 1]
		if dir == 2:
			return [self.x + 1, self.y]
		if dir == 3:
			return [self.x + 1, self.y + 1]
		if dir == 4:
			return [self.x, self.y + 1]
		if dir == 5:
			return [self.x - 1, self.y + 1]
		if dir == 6:
			return [self.x - 1, self.y]
		if dir == 7:
			return [self.x - 1, self.y - 1]

	# узнаём кол-во феромона на соседних клетках
	def getFeromone(self, dir, field):
		feromoneX = self.x
		feromoneY = self.y
		if dir == 0:
			feromoneY = self.y - 1
		if dir == 1:
			feromoneY = self.y - 1
			feromoneX = self.x + 1
		if dir == 2:
			feromoneX = self.x + 1
		if dir == 3:
			feromoneX = self.x + 1
			feromoneY = self.y + 1
		if dir == 4:
			feromoneY = self.y + 1
		if dir == 5:
			feromoneY = self.y + 1
			feromoneX = self.x - 1
		if dir == 6:
			feromoneX = self.x - 1
		if dir == 7:
			feromoneX = self.x - 1
			feromoneY = self.y - 1

		if type(field.matrix[feromoneX][feromoneY]) == type(0.0):			
			return field.matrix[feromoneX][feromoneY]
		else:
			return const.initFeromone * 10000

	# функция возвращает величину, обратную расстоянию
	def getInverseDistance(self, dir):
		if (dir == 0) or (dir == 2) or (dir == 4) or (dir == 6):
			return 1.0 # по прямой расстояние равно 1
		else:
			return float(1 / 2 ** .5) # по диагонали расстояние равно корню из 2

	#определяем возможные ходы (проверка на наличие в табу листе)
	possibleTurns = []	
	def addPossibleTurns(self, arr, field):
		self.possibleTurns = []
		for i in arr:
			pp = self.tryMove(i)
			if not(pp in self.tabooList) and (pp[0] in range(0, 100)) and (pp[1] in range(0, 100)) and (field.matrix[pp[0]][pp[1]] != "obstacle"):
				self.possibleTurns.append(i)

	#обнуляем муравья, когда он "заблудился"
	def respawn(self, field):
		self.x = const.spawnX
		self.y = const.spawnY
		self.tabooList = []
		self.putFeromone = False
		self.tabooListIndex = 0
		self.l0 = 0

	# выбираем куда идти и идём туда
	def turn(self, field):
		if not self.putFeromone:

			# задаём возможные направления
			if (self.x == 0) and (self.y == 0):
				self.addPossibleTurns([2, 3, 4], field)
			if (self.x == 0) and (self.y == 99):
				self.addPossibleTurns([0, 1, 2], field)
			if (self.x == 99) and (self.y == 0):
				self.addPossibleTurns([4, 5, 6], field)
			if (self.x == 99) and (self.y == 99):
				self.addPossibleTurns([6, 7, 0], field)
			if (self.x == 0) and (self.y in range(1, 99)):
				self.addPossibleTurns([0, 1, 2, 3, 4], field)
			if (self.x == 99) and (self.y in range(1, 99)):
				self.addPossibleTurns([0, 4, 5, 6, 7], field)
			if (self.y == 0) and (self.x in range(1, 99)):
				self.addPossibleTurns([2, 3, 4, 5, 6], field)
			if (self.y == 99) and (self.x in range(1, 99)):
				self.addPossibleTurns([6, 7, 0, 1, 2], field)
			if (self.x in range(1, 99)) and (self.y in range(1, 99)):
				self.addPossibleTurns([0, 1, 2, 3, 4, 5, 6, 7], field)
			
			# вычисляем вероятность хода
			summ = 0
			probabilities = []
			for i in self.possibleTurns:
				summ += self.getInverseDistance(i) ** const.beta * self.getFeromone(i, field) ** const.alpha
			for i in self.possibleTurns:
				probabilities.append(self.getInverseDistance(i) ** const.beta * self.getFeromone(i, field) ** const.alpha / summ )

			if not self.leet:
				# функция подсчитывает сумму первых элементов массива
				def sumFirstElements(arr, end):
					summ = 0
					if end >= len(arr):
						end = len(arr) - 1
					for i in range(0, end):
						summ += arr[i]
					return summ	

				# случайно выбираем направление
				probRange = []
				for i in range(0, len(probabilities)):
					probRange.append(sumFirstElements(probabilities, i))

				def selectDir():
					if (len(self.possibleTurns) > 0):
						rand = r.random()	
						for i in range(len(probRange) - 1):
							if (rand >= probRange[i]) and (rand < probRange[i+1]):
								return self.possibleTurns[i]
						if rand >= probRange[-1]:
							return self.possibleTurns[-1]
					else:
						self.respawn(field)
			else:
				def selectDir():
					if (len(self.possibleTurns) > 0):
						maxProb = max(probabilities)
						maxIndexes = [i for i, j in enumerate(probabilities) if j == maxProb]
#						maxIndexes = []
#						for i, j in enumerate(probabilities):
#							if j == maxProb:
#								maxIndexes.append(i)
						
						return self.possibleTurns[r.choice(maxIndexes)]
					else:
						self.respawn(field)

			self.newDir = selectDir()
			self.move(self.newDir)

			if (field.matrix[self.x][self.y] == "food"):
				self.putFeromone = True

				if (const.initialFoodAmount != 0):
					field.foodAmounts[field.foodList.index([self.x, self.y])] -= 1
					if field.foodAmounts[field.foodList.index([self.x, self.y])] == 0:
						field.matrix[self.x][self.y] = const.initFeromone
						self.putFeromone = False
				
		else: #if putFeromone
			oldX = self.x
			oldY = self.y
			self.tabooListIndex += 1
			self.x = self.tabooList[-self.tabooListIndex][0]
			self.y = self.tabooList[-self.tabooListIndex][1]
			dx = self.x - oldX
			dy = self.y - oldY
			if (dx == 0) and (dy == -1):
				self.newDir = 0
			if (dx == 1) and (dy == -1):
				self.newDir = 1
			if (dx == 1) and (dy == 0):
				self.newDir = 2
			if (dx == 1) and (dy == 1):
				self.newDir = 3
			if (dx == 0) and (dy == 1):
				self.newDir = 4
			if (dx == -1) and (dy == 1):
				self.newDir = 5
			if (dx == -1) and (dy == 0):
				self.newDir = 6
			if (dx == -1) and (dy == -1):
				self.newDir = 7
			
			if type(field.matrix[self.x][self.y]) == type(0.0):
				newTau = (1 - const.p) * field.matrix[self.x][self.y] + const.q / self.l0
				field.matrix[self.x][self.y] = newTau

			if (field.matrix[self.x][self.y] == "spawn"):
				self.respawn(field)	
		return
	
# Create your models here.

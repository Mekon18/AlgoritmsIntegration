from django.db import models

class Const(models.Model):
	class Meta:
		app_label='Const'
	id = models.IntegerField(primary_key=True)
	scale = models.IntegerField(default = 6) # масштаб графического окна
	spawnX = models.IntegerField(default = 50)
	spawnY = models.IntegerField(default = 50)
	numAnts = models.IntegerField(default = 50) # общее кол-во муравьев
	leetQ = models.IntegerField(default = 5) # процент элитных муравьев
	initFeromone = models.FloatField(default = 1.0) # начальное значение феромона

	numFood = models.IntegerField(default = 30) # количество еды
	minFoodDistance = models.IntegerField(default = 20) #минимальное расстояние до еды по каждой стороне
	maxFoodDistance = models.IntegerField(default = 100) #максимальное расстояние до еды по каждой стороне
	initialFoodAmount = models.IntegerField(default = 50) # начальное количество еды
	numObstacles = models.IntegerField(default = 400)# кол-во препятствий
	freeSpace = models.IntegerField(default = 3) #свободное пространство, оставляемое вокруг спавна и еды

	# параметры алгоритма
	alpha = models.IntegerField(default = 3) # степень количества феромона (влияет на вероятность пойти туда, где его больше)
	beta = models.IntegerField(default = 3) # степень величины, обратной расстоянию (в данном случае, влияет на приоритет ходов по прямой)
	q = models.IntegerField(default = 100) # множитель на величину обратную пройденному пути (кол-во оставляемого феромона)
	p = models.FloatField(default = 0.0003) # локальный коэффицицент испарения
	gp = models.FloatField(default = 0.0007) # глобальный коэффицицент испарения
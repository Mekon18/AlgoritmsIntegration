from Ants.const import *
import app.models as mod

class Draw:

	def getDrawingMatrix(self, field):
		drawingMatrix = []
		for i in range(100):
			drawingMatrix.append([])
			for j in range(100):
				drawingMatrix[i].append(WHITE)
				if field.matrix[i][j] == "spawn":
					drawingMatrix[i][j] = "spawn"
				elif field.matrix[i][j] == "food":
					drawingMatrix[i][j] = "food"
				elif field.matrix[i][j] == "obstacle":
					drawingMatrix[i][j] = "obstacle"
				else: drawingMatrix[i][j] = "free"
		# отрисовка и  ход муравьёв
		for ant in field.ants:
			if (ant.newDir == 0) or (ant.newDir == 1) or (ant.newDir == 7):
				drawingMatrix[ant.x][ant.y] = "antUp"
			if ant.newDir == 2:
				drawingMatrix[ant.x][ant.y] = "antRight"
			if (ant.newDir == 3) or (ant.newDir == 4) or (ant.newDir == 5):
				drawingMatrix[ant.x][ant.y] = "antDown"
			if ant.newDir == 6:
				drawingMatrix[ant.x][ant.y] = "antLeft"
			mod.CoordinateAnts.objects.create(x = ant.x, y = ant.y)
		return drawingMatrix

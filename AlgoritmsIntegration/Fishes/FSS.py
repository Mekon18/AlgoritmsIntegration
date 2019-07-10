import random
import math


class Point:

    def __init__(self,X = 0 ,Y = 0,Z = 0, weight = 0):
        if not isinstance(X,Point):
            self.X = X
            self.Y = Y
            self.Z = Z
            self.weight = weight
        else:
            self.X = X.X
            self.Y = X.Y
            self.Z = X.Z
            self.weight = X.weight

    def copy(self,point):
        self.X = point.X
        self.Y = point.Y
        self.Z = point.Z
        self.weight = point.weight


    def dist(self,point):
        return ((self.X - point.X)**2 + (self.Y - point.Y)**2)**.5

class Functions:

    @staticmethod
    def GetValue(n,x,y):
        if n == 1:
            return ((x**2 + y - 11)**2 + (x + y**2 - 7)**2)
        else:
            if n == 2:
                return ((1 - x)**2 + 100 * (y - x**2)**2)
            else:
                if n == 3:
                    return (x**2 + y**2)
                else:
                    if n == 4:
                        return (20 + (x**2 - 10 * math.cos(2*math.pi*x)) + (y**2 - 10 * math.cos(2*math.pi*y)))
                    else:
                        if n == 5:
                            return -20 * math.exp(-0.2 * math.sqrt(0.5 * x**2 * y**2)) - math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))) + math.e + 20


class Fish:
    def __init__(self, weightMax,speed,n,MinX,MaxX,MinY,MaxY):
        self.weightMax = weightMax
        self.weightNew = weightMax / 2
        self.speedX = speed
        self.speedY = speed
        self.speed = speed
        self.MinX = MinX
        self.MaxX = MaxX
        self.MinY = MinY
        self.MaxY = MaxY
        self.n = n
        self.points = [Point(0) for i in range(4)]
        self.IndividDeltaFitness = 0
        self.weightOld = weightMax / 2


    def SearchIndividDeltaFitness(self):
        # self.IndividDeltaFitness = self.points[2].Z - self.points[1].Z
        self.IndividDeltaFitness = self.points[2].Z - self.points[0].Z

    def GenInitalPosition(self):
        X = random.uniform(self.MinX, self.MaxX)
        Y = random.uniform(self.MinY, self.MaxY)
        Z = Functions.GetValue(self.n, X, Y)
        self.points[0] = Point(X,Y,Z)

    def fitness(self, point):
        point.Z = Functions.GetValue(self.n,point.X, point.Y)

    def IndividualMovements(self):
        self.speedX = self.speed * random.uniform(-1,1)
        self.speedY = self.speed * random.uniform(-1,1)
        newPoint = Point(0)
        newPoint.X = self.points[0].X + self.speedX
        newPoint.Y = self.points[0].Y + self.speedY
        self.fitness(newPoint)
        if (newPoint.X <= self.MaxX) and (newPoint.X >= self.MinX) and (newPoint.Y <= self.MaxY) and (newPoint.Y >= self.MinY) and (newPoint.Z <= self.points[0].Z):
            self.points[1].copy(newPoint)
        else:
            self.points[1].copy(self.points[0])

class FishSchool:

    def __init__(self,iterationCount,populationSize, weightMax = 0,speed = 0, n = 0 , MinX = 0,MaxX = 0,MinY = 0,MaxY = 0):
        self.populationSize = populationSize
        self.fishes = [Fish(weightMax,speed,n,MinX,MaxX,MinY,MaxY) for i in range (populationSize)]
        self.MsjX = 0
        self.MsjY = 0
        self.MaxDeltaFitness = 0
        self.barycentre = Point(0)
        self.iterationCount = iterationCount

    def GetIndirectInteraction(self):
        numeratorX = 0
        numeratorY = 0
        denumerator = 0
        for i in range (self.populationSize):
            numeratorX += self.fishes[i].speedX * (self.fishes[i].points[1].Z - self.fishes[i].points[0].Z)
            numeratorY += self.fishes[i].speedY * (self.fishes[i].points[1].Z - self.fishes[i].points[0].Z)
            denumerator += self.fishes[i].points[1].Z - self.fishes[i].points[0].Z
        if denumerator != 0:
            self.MsjX = numeratorX/denumerator
            self.MsjY = numeratorY/denumerator

    def InstinctiveCollectiveMovements(self):
        newPoint = Point(0)
        for i in range(self.populationSize):
            self.fishes[i].IndividualMovements()
        self.GetIndirectInteraction()
        for i in range(self.populationSize):
            newPoint.X = self.fishes[i].points[1].X + self.MsjX
            newPoint.Y = self.fishes[i].points[1].Y + self.MsjY
            self.fishes[i].fitness(newPoint)
            if (newPoint.X <= self.fishes[i].MaxX) and (newPoint.X >= self.fishes[i].MinX) and (newPoint.Y <= self.fishes[i].MaxY) and (newPoint.Y >= self.fishes[i].MinY):
                self.fishes[i].points[2].copy(newPoint)
                self.fishes[i].fitness(self.fishes[i].points[2])
            else:
                if (newPoint.X > self.fishes[i].MaxX) and (newPoint.Y > self.fishes[i].MaxY):
                    self.fishes[i].points[2] = Point(self.fishes[i].MaxX,self.fishes[i].MaxY)
                    self.fishes[i].fitness(self.fishes[i].points[2])
                else:
                    if (newPoint.X < self.fishes[i].MinX) and (newPoint.Y < self.fishes[i].MinY):
                        self.fishes[i].points[2] = Point(self.fishes[i].MinX,self.fishes[i].MinY)
                        self.fishes[i].fitness(self.fishes[i].points[2])
                    else:
                            if (newPoint.X > self.fishes[i].MaxX) and (newPoint.Y < self.fishes[i].MaxY) and (newPoint.Y > self.fishes[i].MinY):
                                self.fishes[i].points[2] = Point(self.fishes[i].MaxX, newPoint.Y)
                                self.fishes[i].fitness(self.fishes[i].points[2])
                            else:
                                if (newPoint.X < self.fishes[i].MinX) and (newPoint.X < self.fishes[i].MaxY) and (newPoint.Y > self.fishes[i].MaxY):
                                    self.fishes[i].points[2] = Point(self.fishes[i].MinX, newPoint.Y)
                                    self.fishes[i].fitness(self.fishes[i].points[2])
                                else:
                                    if (newPoint.X < self.fishes[i].MaxX) and (newPoint.X > self.fishes[i].MinX) and (newPoint.Y > self.fishes[i].MaxY):
                                        self.fishes[i].points[2] = Point(newPoint.X, self.fishes[i].MaxY)
                                        self.fishes[i].fitness(self.fishes[i].points[2])
                                    else:
                                        if (newPoint.X < self.fishes[i].MaxX) and (newPoint.X > self.fishes[i].MinX) and (newPoint.Y < self.fishes[i].MinY):
                                            self.fishes[i].points[2] = Point(newPoint.X, self.fishes[i].MinY)
                                            self.fishes[i].fitness(self.fishes[i].points[2])
                                        else:
                                            if (newPoint.X > self.fishes[i].MaxX) and (newPoint.Y < self.fishes[i].MinY):
                                                self.fishes[i].points[2] = Point(self.fishes[i].MaxX, self.fishes[i].MinY)
                                                self.fishes[i].fitness(self.fishes[i].points[2])
                                            else:
                                                if (newPoint.X < self.fishes[i].MinX) and (newPoint.Y > self.fishes[i].MaxY):
                                                    self.fishes[i].points[2] = Point(self.fishes[i].MinX, self.fishes[i].MaxY)
                                                    self.fishes[i].fitness(self.fishes[i].points[2])

    def SearchMaxDeltaFitness(self):
        for i in range(len(self.fishes)):
            self.fishes[i].SearchIndividDeltaFitness()
        DeltaFitness = [self.fishes[i].IndividDeltaFitness for i in range (len(self.fishes))]
        DeltaFitness_abs = [abs(self.fishes[i].IndividDeltaFitness) for i in range(len(self.fishes))]
        temp_MaxDeltaFitness = max(DeltaFitness_abs)
        temp = DeltaFitness_abs.index(temp_MaxDeltaFitness)
        self.MaxDeltaFitness = DeltaFitness[temp]

    def NewWeight(self):
        self.SearchMaxDeltaFitness()
        for i in range(len(self.fishes)):
            temp = self.fishes[i].weightOld
            self.fishes[i].weightOld = self.fishes[i].weightNew
            if self.MaxDeltaFitness !=0 :
                # self.fishes[i].weightNew = temp + (self.fishes[i].IndividDeltaFitness / self.MaxDeltaFitness)
                self.fishes[i].weightNew = int(temp + self.fishes[i].IndividDeltaFitness / self.MaxDeltaFitness)

            if self.fishes[i].weightNew >= self.fishes[i].weightMax:
                self.fishes[i].weightNew = self.fishes[i].weightMax
            if self.fishes[i].weightNew <= 1:
                self.fishes[i].weightNew = 1

    def SearchBarycentre(self):
        numeratorX = 0
        denumerator = 0
        numeratorY = 0
        for i in range(len(self.fishes)):
            numeratorX += self.fishes[i].points[2].X * self.fishes[i].weightNew
            numeratorY += self.fishes[i].points[2].Y * self.fishes[i].weightNew
            denumerator += self.fishes[i].weightNew
        self.barycentre.X = numeratorX / denumerator
        self.barycentre.Y = numeratorY / denumerator

    def CollectiveMovements(self):
        self.InstinctiveCollectiveMovements()
        self.NewWeight()
        self.SearchBarycentre()
        newPoint = [Point(0) for i in range (len(self.fishes))]
        sumWeightOld = 0
        sumWeightNew = 0
        for i in range (len(self.fishes)):
            sumWeightOld += self.fishes[i].weightOld
            sumWeightNew += self.fishes[i].weightNew

        if (sumWeightNew < sumWeightOld):
            for i in range(len(self.fishes)):
                newPoint[i].X = self.fishes[i].points[2].X + (2 * self.fishes[i].speed * random.random() * ((self.fishes[i].points[2].X - self.barycentre.X)))
                newPoint[i].Y = self.fishes[i].points[2].Y + (2 * self.fishes[i].speed * random.random() * ((self.fishes[i].points[2].Y - self.barycentre.Y)))
                self.fishes[i].fitness(newPoint[i])
        else:
            for i in range(len(self.fishes)):
                 newPoint[i].X = self.fishes[i].points[2].X - (2 * self.fishes[i].speed * random.random() * ((self.fishes[i].points[2].X - self.barycentre.X)))
                 newPoint[i].Y = self.fishes[i].points[2].Y - (2 * self.fishes[i].speed * random.random() * ((self.fishes[i].points[2].Y - self.barycentre.Y)))
                 self.fishes[i].fitness(newPoint[i])

        for i in range(len(self.fishes)):
            if (newPoint[i].X <= self.fishes[i].MaxX) and (newPoint[i].X >= self.fishes[i].MinX) and (newPoint[i].Y <= self.fishes[i].MaxY) and (newPoint[i].Y >= self.fishes[i].MinY) and (newPoint[i].Z <= self.fishes[i].points[2].Z):
                self.fishes[i].points[3].copy(newPoint[i])
            else:
                self.fishes[i].points[3].copy(self.fishes[i].points[2])

    def ResMovements(self):
        self.CollectiveMovements()
        for i in range(len(self.fishes)):
            #self.fishes[i].speed -= (self.fishes[i].speed - 0.1*self.fishes[i].speed) / self.iterationCount
            self.fishes[i].speedX = self.fishes[i].speed
            self.fishes[i].speedY = self.fishes[i].speed
            self.fishes[i].points[0].copy(self.fishes[i].points[3])

class FSS:

     # def __init__(self,iterationCount, populationSize, mweight = 0,speed = 0, n = 0 , MinX = 0,MaxX = 0,MinY = 0,MaxY = 0):
     #     self.iterationCount = iterationCount
     #     self.populationSize = populationSize
     #     self.FS = FishSchool(iterationCount, populationSize, mweight, speed, n, MinX ,MaxX ,MinY ,MaxY)

     @staticmethod
     def Run(iterationCount, populationSize, mweight = 0,speed = 0, n = 0 , MinX = 0,MaxX = 0,MinY = 0,MaxY = 0):

         FS = FishSchool(iterationCount, populationSize, mweight, speed, n, MinX, MaxX, MinY, MaxY)

         result = [[Point(0)] * (len(FS.fishes)) for i in range(iterationCount)]

         for i in range(len(FS.fishes)):
             FS.fishes[i].GenInitalPosition()
             result[0][i] = Point(FS.fishes[i].points[0])
             result[0][i].weight = FS.fishes[i].weightOld

         for i in range (1,iterationCount):
             FS.ResMovements()
             for j in range(len(FS.fishes)):
                 result[i][j] = Point(FS.fishes[j].points[3])
                 result[i][j].weight = FS.fishes[j].weightOld

         return result
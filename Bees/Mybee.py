import random

class Mybee():        
    def __init__(self,id,function):
        self.minval = [0, 0]
        self.maxval = [500, 500]
        self.id = id
        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(2) ]
        self.Function = function
        self.fitness = self.Function(self.position)

    #def calcfitness(self):
    #    """Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
    #    Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
    #    self.fitness = 0.0
    #    for val in self.position:
    #        self.fitness -= (-250 + val) * (-250 + val)

    def getposition(self):
        """Вернуть копию (!) своих координат"""
        return [val for val in self.position]

    def getMyposition(self):
        """Вернуть копию (!) своих координат"""
        return [self.position[0],self.position[1],self.fitness]

    def otherpatch(self, bee_list, range_list):
        """Проверить находится ли пчела на том же участке, что и одна из пчел в bee_list. 
        range_list - интервал изменения каждой из координат"""
        if len(bee_list) == 0:
        	return True
        
        for curr_bee in bee_list:
        	position = curr_bee.getposition()
        	
        	for n in range(len(self.position)):
        		if abs(self.position[n] - position[n]) > range_list[n]:
        			return True
        
        return False

    def gotorandom(self):
        # Заполним координаты случайными значениями
        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(len(self.position)) ]
        self.checkposition()
        self.fitness = self.Function(self.position)

    def goto(self, otherpos, range_list):
        """Перелет в окрестность места, которое нашла другая пчела. Не в то же самое место! """

		# К каждой из координат добавляем случайное значение
        self.position = [otherpos[n] + random.uniform(-range_list[n], range_list[n]) \
            for n in range(len(otherpos)) ]

        # Проверим, чтобы не выйти за заданные пределы
        self.checkposition()

    def checkposition(self):
        """Скорректировать координаты пчелы, если они выходят за установленные пределы"""
        for n in range(len(self.position)):
        	if self.position[n] < self.minval[n]:
        		self.position[n] = self.minval[n]
        		
        	elif self.position[n] > self.maxval[n]:
        		self.position[n] = self.maxval[n]
import copy

class hive:
	"""Улей. Управляет пчелами"""
	def __init__(self, scoutbeecount, selectedbeecount, bestbeecount, \
				selsitescount, bestsitescount, \
				range_list, beetype,function,iterationcount):
		"""scoutbeecount - Количество пчел-разведчиков
		selectedbeecount - количество пчел, посылаемое на один из лучших участков
		selectedbeecount - количество пчел, посылаемое на остальные выбранные участки
		
		selsitescount - количество выбранных участков
		bestsitescount - количество лучших участков среди выбранных
		beetype - класс пчелы, производный от bee
		
		range_list - список диапазонов координат для одного участка"""
		
		self.iterationcount = iterationcount
		self.scoutbeecount = scoutbeecount
		self.selectedbeecount = selectedbeecount
		self.bestbeecount = bestbeecount		
		
		self.selsitescount = selsitescount
		self.bestsitescount = bestsitescount
		
		self.beetype = beetype
		
		self.range = range_list
		
		# Лучшая на данный момент позиция
		self.bestposition = None
		
		# Лучшее на данный момент здоровье пчелы (чем больше, тем лучше)
		self.bestfitness = -1.0e9
		
		# Начальное заполнение роя пчелами со случайными координатами
		beecount = scoutbeecount + selectedbeecount * selsitescount + bestbeecount * bestsitescount
		self.Function = function
		self.swarm = [beetype(n,function) for n in range(beecount)]
		
		# Лучшие и выбранные места
		self.bestsites = []
		self.selsites = []

		self.swarm.sort(key=lambda elem : elem.fitness , reverse = True)		
		self.bestposition = self.swarm[0].getposition()
		self.bestfitness = self.swarm[0].fitness
	
	def sendbees(self, position, index, count):
		""" Послать пчел на позицию.
		Возвращает номер следующей пчелы для вылета """
		for n in range(count):
			# Чтобы не выйти за пределы улея
			if index == len(self.swarm):
				break
			
			curr_bee = self.swarm[index]
			
			if curr_bee not in self.bestsites and curr_bee not in self.selsites:
				# Пчела не на лучших или выбранных позициях
				curr_bee.goto(position, self.range)
			
			index += 1
		
		return index
	
	def nextstep(self):
		"""Новая итерация"""		
		# Выбираем самые лучшие места и сохраняем ссылки на тех, кто их нашел		
		self.swarm.sort(key=lambda elem : elem.fitness , reverse = True)
		self.bestsites = [self.swarm[0]]
		
		curr_index = 1
		for currbee in self.swarm[curr_index: -1]:
			# Если пчела находится в пределах уже отмеченного лучшего участка, то ее
			# положение не считаем
			if currbee.otherpatch(self.bestsites, self.range):
				self.bestsites.append(currbee)
						
				if len(self.bestsites) == self.bestsitescount:
					break
				
			curr_index += 1
		
		self.selsites = []
		
		for currbee in self.swarm[curr_index: -1]:
			if currbee.otherpatch(self.bestsites, self.range) and currbee.otherpatch(self.selsites, self.range):
				self.selsites.append(currbee)
					
				if len(self.selsites) == self.selsitescount:
					break
					
		# Отправляем пчел на задание :)
		# Отправляем сначала на лучшие места
		
		# Номер очередной отправляемой пчелы.  0-ую пчелу никуда не отправляем
		bee_index = 1
		
		for best_bee in self.bestsites:
			bee_index = self.sendbees(best_bee.getposition(), bee_index, self.bestbeecount)
			
		for sel_bee in self.selsites:
			bee_index = self.sendbees(sel_bee.getposition(), bee_index, self.selectedbeecount)	

		# Оставшихся пчел пошлем куда попадет
		for curr_bee in self.swarm[bee_index: -1]:
			curr_bee.gotorandom()

		self.swarm.sort(key=lambda elem : elem.fitness , reverse = True)		
		self.bestposition = self.swarm[0].getposition()
		self.bestfitness = self.swarm[0].fitness
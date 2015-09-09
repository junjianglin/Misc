# Online ad scheduling problem, selection part, details please see the group interview guide.

class Area():
	"""
	Attributes:
	    weight: the multiplier of this area
	    id: unique id
	    w: content candidates, a list with 3 lists
	"""
	def __init__(self,id,weight):
		self.weight = weight
		self.id = id
		#this design is not suitable, store w1,w2,w3 in a list called wait
		self.w = [[None]*20 for _ in range(3)]

	def addContent(self,wait,start,content):
		if self.checkAddContent(wait,start,content):
			for i in range(content.length):
				self.w[wait][start+i] = (start+i,content)
		else:
			print content,"can not override existing content"

	def checkAddContent(self,wait,start,content):
		"""return True if the waiting_area can hold content
		"""
		for i in range(content.length):
			if start+i > 19:
				return False
			elif self.w[wait][start+i] != None:
				return False
		return True

	def delContent(self,wait,start,content):
		for i in range(content.length):
			self.w[wait][start+i] = None

	def printSchedule(self):
		self.printWaiting()
		print ' '.join(map(format,range(20),['2' for _ in\
						range(20)]))
		print ""

	def printWaiting(self):
		for wait in self.w:
			w_print=""
			for c in wait:
				if c:
					w_print += str(c[1])
				else:
					w_print += 'NO'
				w_print += " "
			print w_print

	def __cmp__(self,o):
		return cmp(self.weight,o.weight)

	def __repr__(self):
		return self.id

class Content():
	def __init__(self,id,length,value):
		self.id = id
		self.length = length
		self.value = value

	def __cmp__(self,o):
		if o != None:
			return cmp(self.value,o.value)
		else:
			return cmp(self.value,0)

	def __eq__(self,other):
		if other != None:
			return self.id==other.id and \
				   self.length == other.length and \
				   self.value==other.value
		else:
			return False

	def __repr__(self):
		return 'c'+str(self.id)

class Selection_solution():
	def select_bruteforce(self,time,a1,a2,*args):
		"""Combinatorial search algorithm,
			Given area1, and area2 ...and a given time,
			return a selection, which maximize total
			weights, O(n^k), k is the number of areas, n is the					   the number of waiting contents in each areas in one time
			Algo:
			Backtrack to generate all solution and compare with
			current best solution, if it is better, replace current
			best with new one
		"""
		areas = []
		areas.append(a1)
		areas.append(a2)
		areas.extend(args)
		candidates = [[wait[time][1] if wait[time]!=None else None \
					  for wait in area.w] for area in areas]
		weights = [area.weight for area in areas]
		input = (candidates,weights)
		best = [None]*len(candidates)
		a = [-1]*len(areas)
		k = -1
		self.backtrack(a,k,input,best)
		print 'bruteforce optimal solution,',zip(areas,best)
		print 'bruteforce optimal cost,',sum([x.value*y for x,y in \
										 zip(best,weights)])

	def calculateCost(self,sol,weights):
		return sum([x.value*y if x != None else 0 \
					for x,y in zip(sol,weights)])

	def backtrack(self,a,k,input,best):
		if k == len(input[0])-1:
			best_cost = self.calculateCost(best,input[1])
			cur_cost = self.calculateCost(a,input[1])
			#print "cur_sol,cur_cost,best_sol,best_cost",\
			#		a,cur_cost,best,best_cost
			if cur_cost > best_cost:
				for idx,content in enumerate(a):
					best[idx] = a[idx]
		else:
			k += 1
			if k == 0:
				c = input[0][k]
				ncandidates = len(c)
			else:
				#print a, input[0][k]
				c = [x for x in input[0][k] if (x==None) or \
					(a[k-1]==None) or (x.id!=a[k-1].id)]
				ncandidates = len(c)

			for i in range(ncandidates):
				a[k] = c[i]
				self.backtrack(a,k,input,best)

	def select_greedy(self,time,a1,a2,*args):
		"""greedy algorithm, take the most weight area first, and
		   give it most valuable content, then second area, and
		   so on , O(klogk + knlogn), not optimal, but efficient
		   Algo:
		   sort area by their weight in descreasing order, and choose
		   the most valuable content in the area, and then second area
		   ,keep checking whether the content have been selected by
		   previous area
		"""
		areas = []
		areas.append(a1)
		areas.append(a2)
		areas.extend(args)
		areas_sorted = sorted(areas,cmp=lambda x,y:\
						cmp(y.weight,x.weight))
		result = []
		candidates = [[wait[time][1] if wait[time]!=None else None \
					  for wait in area.w] for area in areas]
		used_content = set()
		for area,cands in zip(areas_sorted,candidates):
			cands.sort(cmp = lambda x,y:cmp(y,x))
			for i in range(len(cands)):
				if cands[i] == None:
					result.append((area,None))
					break
				else:
					if cands[i].id not in used_content:
						result.append((area,cands[i]))
						used_content.add(cands[i].id)
						break
		print "greedy best solution:",result
		print "greedy best cost:",sum([x.weight*y.value if y!= None \
									else 0 for x,y in result])
class Schedule_solution():
	def schedule_randomSampling(self,contents,areas):
		""" random Sampling method, or Monte Carlo
			Algo: Generating random result first, and
			    then check whether it is valid, if not
			    valid, re-generate a random one, until
			    it is valid.
		"""
		solutions = []
		for i in range(len(areas)):
			while True:
				schedule = self.randomSchedule(contents)
				if self.validSchedule(schedule)[0]:
					schedule.id = "area" + str(i+1)
					solutions.append(schedule)
					break
				else:
					pass
					#print "not valid"
		for sol in solutions:
			sol.printSchedule()
		return solutions
	def randomSchedule(self,contents):
		import random as ran
		contents_copy = contents[:]
		sol = Area('sb',ran.random())
		while contents_copy:
			cont = ran.choice(contents_copy)
			i = 0
			while True:
				ran_waiting = ran.randint(0,2)
				ran_start = ran.randint(0,19)
				if sol.checkAddContent(ran_waiting,ran_start,cont):
					sol.addContent(ran_waiting,ran_start,cont)
					contents_copy.remove(cont)
					break
				i += 1
				if i>150:
					#print "cut"
					sol = Area('sb',ran.random())
					contents_copy = contents[:]
					break
		#print "generate new schedule\n",sol.printSchedule()
		return sol

	def validSchedule(self,schedule):
		def validRow(content,start,row):
			cur_id = content[1].id
			try:
				next_c = row[start+content[1].length]
			except IndexError:
				return True
			if next_c != None:
				if cur_id != next_c[1].id:
					return True
				else:
					#print "row not valid"
					return False
			else:
				return True

		def validCol(content,start,schedule):
			cur_id = content[1].id
			#print "cur_id,length,start",cur_id,content[1].length,start
			flag = 0
			for i in range(content[1].length):
				for j in range(len(schedule.w)):
					#print start,i,content[1]
					if schedule.w[j][start+i]!=None and \
						schedule.w[j][start+i][1].id == cur_id:
						flag += 1
			if flag != content[1].length:
				#print "col not valid",flag,content[1].length,cur_id
				return False
			else:
				return True
		def validRowCol(content,start,row,schedule):
			if validRow(content,start,row) and \
				validCol(content,start,schedule):
				return True
			else:
				return False

		i = 0
		while i < len(schedule.w):
			j = 0
			while j < len(schedule.w[i]):
				c = schedule.w[i][j]
				if c != None:
					if not validRowCol(c,j,schedule.w[i],schedule):
						return False,(c,i)
					else:
						j += c[1].length
				else:
					j += 1
			i += 1
		return True,None

	def schedule_localSearch(self,contents,areas):
		""" local greedy search
		Algo: randomly generate a schedule, if not valid,
		    find the content that result in invalid, and switch it
		    with other random content, check whether it is valid
		    again, until we get a valid one
		"""
		solutions = []
		for i in range(len(areas)):
			schedule = self.randomSchedule(contents)
			count = 0
			while True:
				if self.validSchedule(schedule)[0]:
					schedule.id = "area"+str(i+1)
					solutions.append(schedule)
					count = 0
					break
				else:
					schedule = self.transition(schedule)
					count += 1
					if count > 10:
						count = 0
						schedule = self.randomSchedule(contents)
		for sol in solutions:
			sol.printSchedule()

	def transition(self,schedule):
		""" use validSchedule to find the problematic content,
			and switch it with another random content
		"""
		c_p = self.validSchedule(schedule)[1]
		row = c_p[1]
		start = c_p[0][0]
		c = c_p[0][1]
		space = c.length
		start_new = start
		for i in range(19):
			try:
				if schedule.w[row][start-i-1] == None:
					space += 1
					start_new -= 1
				else:
					break
			except IndexError:
				break
		for i in range(19):
			try:
				if schedule.w[row][start+i+1] == None:
					space += 1
				else:
					break
			except IndexError:
				break

		for i in range(len(schedule.w)):
			j = 0
			while j < len(schedule.w[i]) and (j<start or j>start+c.length):
				if schedule.w[i][j] != None and schedule.w[i][j][1].length\
				   <=space and schedule.w[i][j][1].id!=c.id\
				   and c.length<=schedule.w[i][j][1].length:
					temp = i,j,schedule.w[i][j][1]
					schedule.delContent(temp[0],temp[1],temp[2])
					#print "add,",c
					schedule.addContent(temp[0],temp[1],c)
					schedule.delContent(row,start,c)
					#print "add,",temp[2]
					schedule.addContent(row,start_new,temp[2])
				elif schedule.w[i][j] == None:
					j += 1
				else:
					j += schedule.w[i][j][1].length
		return schedule


def mainSelection():
	import timeit
	c1 = Content(1,4,20)
	c2 = Content(2,6,30)
	c3 = Content(3,5,25)
	c1_ = Content(1,1,20)
	c5 = Content(5,3,29)
	c6 = Content(6,11,50)
	c7 = Content(7,7,34)
	c1__ = Content(1,3,20)
	c8 = Content(8,6,10)
	a1 = Area('a1',1.0)
	a1.addContent(0,0,c1)
	a1.addContent(0,6,c2)
	a1.addContent(0,12,c3)
	a1.addContent(0,18,c1_)
	a1.addContent(1,2,c5)
	a1.addContent(1,9,c6)
	a1.addContent(2,0,c7)
	a1.addContent(2,9,c1__)
	a1.addContent(2,14,c8)
	a1.printSchedule()
	print "\n"
	a2 = Area('a2',0.5)
	a2.addContent(0,0,c6)
	a2.addContent(0,11,c7)
	a2.addContent(1,0,c1)
	a2.addContent(1,6,c8)
	a2.addContent(1,15,c3)
	a2.addContent(2,0,c3)
	a2.addContent(2,7,c5)
	a2.addContent(2,13,c2)
	a2.addContent(2,19,c1_)
	a2.printSchedule()
	a3 = Area('a3',1.0)
	a4 = Area('a4',0.9)
	a3.addContent(0,0,c2)
	a3.addContent(1,0,c5)
	a4.addContent(0,0,c2)
	sol_select = Selection_solution()
	time_b = timeit.default_timer()
	sol_select.select_bruteforce(time=12,a1=a1,a2=a2)
	print "running time: ",timeit.default_timer()-time_b
	time_g = timeit.default_timer()
	sol_select.select_greedy(time=12,a1=a1,a2=a2)
	print "running time: ",timeit.default_timer()-time_g
	time_b = timeit.default_timer()
	sol_select.select_bruteforce(time=0,a1=a3,a2=a4)
	print "running time: ",timeit.default_timer()-time_b
	time_g = timeit.default_timer()
	sol_select.select_greedy(time=0,a1=a3,a2=a4)
	print "running time: ",timeit.default_timer()-time_g

def mainSchedule():
	import timeit
	c1 = Content(1,5,20)
	c2 = Content(2,6,30)
	c3 = Content(3,5,25)
	c1_ = Content(1,1,20)
	c5 = Content(5,3,29)
	c6 = Content(6,11,50)
	c7 = Content(7,7,34)
	c1__ = Content(1,3,20)
	c8 = Content(8,6,10)
	a1 = Area('a1',1.0)
	a2 = Area('a2',0.5)
	a3 = Area('a3',0.8)
	contents = [c1,c2,c3,c1_,c5,c6,c7,c1__,c8]
	areas = [a1,a2,a3]
	sol_schedule = Schedule_solution()
	print "random sampling schedule:\n"
	time_r = timeit.default_timer()
	schedule_sols = sol_schedule.schedule_randomSampling(contents,areas)
	print "running time,",timeit.default_timer()-time_r
	print "local search schedule:"
	time_l = timeit.default_timer()
	schedule_sols_local = sol_schedule.schedule_localSearch(contents,areas)
	print "running time,",timeit.default_timer()-time_l
	sol_selection = Selection_solution()
	#sol_selection.select_bruteforce(4,*schedule_sols)     #argument unpacking

if __name__ == '__main__':
	#mainSelection()
	mainSchedule()



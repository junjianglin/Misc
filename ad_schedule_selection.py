# Online ad scheduling problem, selection part, details please see the group interview guide.

class Area():
	def __init__(self,id,weight):
		self.weight = weight
		self.id = id
		self.w1 = [None]*20
		self.w2 = [None]*20
		self.w3 = [None]*20
	
	def updateWaiting(self,w1,w2,w3):
		self.w1 = w1
		self.w2 = w2
		self.w3 = w3

	def addContent(self,waiting_area,start,content):
		w = getattr(self,waiting_area)
		for i in range(content.length):
			if w[start+i] != None:
				print content," can not overrite,",w[start+i]
			else:
				w[start+i] = (start+i,content)
	def checkAddContent(self,waiting_area,start,content):
		"""return True if the waiting_area can hold content
		"""
		w = getattr(self,waiting_area)
		for i in range(content.length):
			if start+i > 19:
				return False
			elif w[start+i] != None:
				return False
		return True

	def printSchedule(self):
		self.printWaiting('w1')
		self.printWaiting('w2')
		self.printWaiting('w3')
		print ' '.join(map(format,range(20),['2' for _ in\
						range(20)]))
		print ""
	def printWaiting(self,wait):
		w_print=""
		w = getattr(self,wait)
		for c in w:
			if c:
				w_print += str(c[1])
			else:
				w_print += 'No'
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
			return self.id==other.id and self.length == other.length\
					and self.value==other.value
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
		candidates = [[x.w1[time][1] if x.w1[time]!=None else None\
					  ,x.w2[time][1] if x.w2[time]!=None else None\
					  ,x.w3[time][1] if x.w3[time]!=None else None]\
					   for x in areas]
		weights = [x.weight for x in areas]
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
		candidates = [[x.w1[time][1] if x.w1[time]!=None else None\
					  ,x.w2[time][1] if x.w2[time]!=None else None\
					  ,x.w3[time][1] if x.w3[time]!=None else None]\
					   for x in areas_sorted]
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
				if self.validSchedule(schedule):
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
				ran_waiting = 'w'+ str(ran.randint(1,3))
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
				if schedule.w1[start+i]!=None and \
					schedule.w1[start+i][1].id == cur_id:
					flag += 1
				if schedule.w2[start+i]!=None and \
					schedule.w2[start+i][1].id == cur_id:
					flag += 1
				if schedule.w3[start+i]!=None and \
					schedule.w3[start+i][1].id == cur_id:
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
		while i < len(schedule.w1):
			c = schedule.w1[i]
			if c != None:
				if not validRowCol(c,i,schedule.w1,schedule):
					return False
				else:
					i += c[1].length
			else:
				i += 1
		i = 0
		while i < len(schedule.w2):
			c = schedule.w2[i]
			if c != None:
				if not validRowCol(c,i,schedule.w2,schedule):
					return False
				else:
					i += c[1].length
			else:
				i += 1
		i = 0
		while i < len(schedule.w3):
			c = schedule.w3[i]
			if c != None:
				if not validRowCol(c,i,schedule.w3,schedule):
					return False
				else:
					i += c[1].length
			else:
				i += 1
	    			
		return True
	
	def schedule_localSearch(self,contents,areas):
		""" local greedy search
		Algo: randomly generate a schedule, if not valid,
			  find the content that result in invalid, and switch it
			  with other random content, check whether it is valid 
			  again, until we get a valid one
		"""
		pass	
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
	a1.addContent('w1',0,c1)
	a1.addContent('w1',6,c2)
	a1.addContent('w1',12,c3)
	a1.addContent('w1',18,c1_)
	a1.addContent('w2',2,c5)
	a1.addContent('w2',9,c6)
	a1.addContent('w3',0,c7)
	a1.addContent('w3',9,c1__)
	a1.addContent('w3',14,c8)
	a1.printSchedule()
	print "\n"
	a2 = Area('a2',0.5)
	a2.addContent('w1',0,c6)
	a2.addContent('w1',11,c7)
	a2.addContent('w2',0,c1)
	a2.addContent('w2',6,c8)
	a2.addContent('w2',15,c3)
	a2.addContent('w3',0,c3)
	a2.addContent('w3',7,c5)
	a2.addContent('w3',13,c2)
	a2.addContent('w3',19,c1_)
	a2.printSchedule()
	a3 = Area('a3',1.0)
	a4 = Area('a4',0.9)
	a3.addContent('w1',0,c2)
	a3.addContent('w2',0,c5)
	a4.addContent('w1',0,c2)
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
	sol_selection = Selection_solution()
	#sol_selection.select_bruteforce(4,schedule_sols[0],schedule_sols[1],schedule_sols[2])
	sol_selection.select_bruteforce(4,*schedule_sols)     #argument unpacking
if __name__ == '__main__':
	#mainSelection()
	mainSchedule()
	


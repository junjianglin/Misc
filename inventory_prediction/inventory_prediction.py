#inventory prediction problem, given orders information and logistics information,
#predict the inventory in next month, details please see groupinterview.doc in
#Company folder

class Order():
	"""
	Attributes:
		orderTime: the time this order generated, datetime
		dest: destination of shipping
		pro: product name
		num: number of products
		time: time allowed to deliver the product, time = arrTime-orderTime
	"""
	def __init__(self,orderTime,dest,pro,num,time):
		self.orderTime = orderTime
		self.dest = dest
		self.pro = pro
		self.num = int(num)
		self.time = int(time)

        def __repr__(self):
            return str(self.orderTime)+" "+self.dest+" "+self.pro+" "+self.num+" "+self.time

class Shipping():
	"""
	Attributes:
		product_shipping: a dict to store (product_name,shipping_info),shipping_info is a
						  dict contains a matrix having delivery cost, each cell in the matrix
						  is list having the cost from 1 day to 3 day
	"""
	def __init__(self):
		self.product_shipping ={}

	def updateShipping(self,pro_list,shipping_info):
		self.product_shipping = dict(zip(pro_list,shipping_info))

class Factory():
    """Factory class to generate parser and order
    """
    def getParser(self,type='re'):
        if type == 're':
            return Parser()
        else:
            print "invalid parser"

    def getOrder(self,ordertime,dest,pro,num,time,type='re'):
        if type == 're':
            return Order(ordertime,dest,pro,num,time)
        else:
            print "invalid order"

class Parser():
    """Parser class parse the input of order and delivery table
    """
    def parseOrder(self,orderFile,skiprow=1):
        """
        parse the order file
        Args:
            skiprow: the number of row to skip
            orderFile: the path to the order file
        Returns:
            a list of order objects
        """
        from datetime import datetime
        factory = Factory()
        f = open(orderFile,'r')
        orders = []
        for _ in range(skiprow):
            f.readline()
        for line in f:
            order = line.split()
            orderTime = datetime(*map(int,order[0].split(':')))
            dest = order[1]
            pro = order[2]
            num = order[3]
            time = order[4]
            order_obj = factory.getOrder(orderTime,dest,pro,num,time)

            orders.append(order_obj)
        return orders
        f.close()

    def parseDelivery(self,deliveryFile,skiprow=0):
        """parse the delivery table info
        Args:
            skiprow: the number of rows to skep
            deliveryFile: the path to the delivery file
        Returns:
            a dict of shipping info, for example,
            {toy:{Beijing:{Shanghai:[10,20,30]}}} means
            the for toy product, ship form Beijing to Shanghai
            will cost 10,20,30 dollars for 1,2,3-day(s) delivery
        """
        f = open(deliveryFile,'r')
        for _ in range(skiprow):
            f.readline()
        products = f.readline().strip().split(',')
        shipping = {pro:dict() for pro in products}
        for line in f:
            line_split = line.split()
            for key in shipping.keys():
                try:
                    shipping[key][line_split[0]][line_split[1]] = map(int,line_split[2:])
                except KeyError:
                    shipping[key][line_split[0]] = dict()
                    shipping[key][line_split[0]][line_split[1]] = map(int,line_split[2:])
        f.close()
        return shipping

class Controller():
    """Controller class

    """
    def __init__(self,model,view):
        self.model = model
        self.view = view

    def calculateInventory(self):
        """calculate the inventory goods for each product
        in each city and each month based on the assumption that
        all goods will choose the latest delivery day
        Returns:
            A dict contains inventory info, for example:
            {toy:{shanghai:{1:20}}} means toy product will have
            20 in shanghai in Jan.
        """
        from collections import Counter
        orders = self.model[0]
        shipping = self.model[1]
        inventory = {key:dict() for key in shipping}
        citys = {o.dest for o in orders}
        months = {o.orderTime.month for o in orders}
        products = {o.pro for o in orders}
        #print shipping
        for pro in products:
            for city in citys:
                inventory[pro][city] = Counter()
        for o in orders:
            o.ship = self.chooseBestShipping(o,citys)

            inventory[o.pro][o.ship][o.orderTime.month] += o.num
        #self.view.showInventory(inventory)
        self.inventory = inventory
        self.citys = citys
        self.months = months
        self.products = products
        return inventory

    def chooseBestShipping(self,order,citys):
        """Choose the best place to ship the product,
        based on the strategy that choose lowest price
        and latest but not too late shipping place
        Args:
            order: the customer order
            citys: all available citys
        Returns:
            the best shipping city
        """
        shipping = self.model[1]
        cur_price = float('inf')
        cur_city = ""
        for city in citys:
            #print city,order.dest
            #print shipping[order.pro][city]
            price = shipping[order.pro][city][order.dest][int(order.time)-1]
            if price < cur_price:
                cur_price = price
                cur_city = city
        return cur_city

    def showInventory(self):
        if not hasattr(self,'inventory'):
            self.calculateInventory()
        self.view.showInventory(self.inventory)

    def showPrediction(self,pre_month,func='predictProduct'):
        if not hasattr(self,'prediction'):
            self.predictAllProducts(pre_month,func)
        self.view.showPredictions(self.prediction)

    def predictAllProducts(self,pre_month,predictfun):
        """ predict all products inventory in a specific month
        Args:
            pre_month: the specific month
        Returns:
            a dict contains the inventory for specific month
            for example, {toy:{shanghai:20}} means store 20 toys
            in shanghai in the specific month
        """
        predictions = {key:{} for key in self.products}
        print self.inventory
        for key in predictions.keys():
            for city in self.citys:
                months = sorted(list(self.months))
                nums = []
                for mon in months:
                    nums.append(self.inventory[key][city][mon])
                func = getattr(self,predictfun)
                predictions[key][city] = func((months,nums),\
                        pre_month)
        self.prediction = predictions
        return predictions

    def predictProductByAve(self,data,pred_month):
        """predict Product using average"""

        return round(float(sum(data[1])/len(data[1])),0)

    def predictProduct(self,data,pred_month):
        """predict Product using 1-d linear regression"""
        try:
            func = self.fit(data[0],data[1])
            return round(func(pred_month),0)
        except ZeroDivisionError:
            return 0

    def fit(fit,X, Y):
    	""" Fitting the line according the data X and Y
    	Args:
    		X: predictor variable
    		Y: reponse variable
    	Returns:
    		line(x): A closure to predict reponse given new data x
    	"""
        import math
    	def mean(Xs):
    		""" Calculate the mean of Xs """
    		return sum(Xs) / len(Xs)

    	m_X = mean(X)
    	m_Y = mean(Y)

    	def std(Xs, m):
    		""" Calculate the std of Xs given the mean of Xs, which is m
    		Args:
    			Xs: the given vector of data
    			m: mean of Xs
    		Returns:
    			std of Xs
    		"""
    		normalizer = len(Xs) - 1
    		return math.sqrt(sum((pow(x - m, 2) for x in Xs)) / normalizer)
    	# assert np.round(Series(X).std(), 6) == np.round(std(X, m_X), 6)

    	def pearson_r(Xs, Ys):
    		""" Calculate the pearson R value given Xs and Ys
    		Args:
    			Xs: predictor
    			Ys: reponse variable
    		Returns:
    			pearson R value for Xs and Ys
    		"""
    		sum_xy = 0
    		sum_sq_v_x = 0
    		sum_sq_v_y = 0

    		for (x, y) in zip(Xs, Ys):
    			var_x = x - m_X
    			var_y = y - m_Y
    			sum_xy += var_x * var_y
    			sum_sq_v_x += pow(var_x, 2)
    			sum_sq_v_y += pow(var_y, 2)
                        #print sum_sq_v_x,sum_sq_v_y
    		return sum_xy / math.sqrt(sum_sq_v_x * sum_sq_v_y)
    	# assert np.round(Series(X).corr(Series(Y)), 6) == np.round(pearson_r(X, Y), 6)

    	r = pearson_r(X, Y)

    	b = r * (std(Y, m_Y) / std(X, m_X))
    	A = m_Y - b * m_X

    	def line(x):
    		""" The line to be returned
    		"""
    		return b * x + A
    	return line





class View():
    """View class
    present the info to console
    """
    def showInventory(self,inventory):
        print inventory

    def showPredictions(self,predictions):
        print predictions


if __name__ == '__main__':
    import time
    factory = Factory()
    parser = factory.getParser()
    orders = parser.parseOrder('./order_input.txt')
    shipping = parser.parseDelivery('./delivery_input.txt')
    model = (orders,shipping)
    view = View()
    control = Controller(model,view)
    control.calculateInventory()
    #control.showInventory()
    time1 = time.time()
    control.showPrediction(5)
    print "1d regression,", time.time()-time1
    time2 = time.time()
    control.showPrediction(5,"predictProductByAve")
    print "ave, ",time.time()-time2

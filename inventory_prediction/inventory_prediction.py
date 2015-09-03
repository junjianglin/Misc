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
		self.num = num
		self.time = time

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

	

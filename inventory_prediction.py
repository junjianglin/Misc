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
		arrTime: required arrival time, datetime
		time: time allowed to deliver the product, time = arrTime-orderTime
	"""
	def __init__(self,orderTime,dest,pro,num,arrTime):
		self.orderTime = orderTime
		self.dest = dest
		self.pro = pro
		self.num = num
		self.arrTime = arrTime
		self.time = self.arrTime - self.orderTime

class Shipping():
	"""
	Attributes:
		product_shipping: a dict to store (product_name,shipping_info),shipping_info is a
						  dict contains (time,matrix), which matrix is the delivery cost 
						  table
	"""
	def __init__(self):
		self.product_shipping ={}
	
	def updateShipping(self,pro_list,shipping_info):
		return dict(zip(pro_list,shipping_info))
	

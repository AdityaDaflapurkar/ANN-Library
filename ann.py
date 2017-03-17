import numpy as np
import random

class DenseNet:
#no. of units in each layer, loss fn and activation fn stored
	def __init__(self, input_dim, optim_config, loss_fn):
		self.net=Graph(input_dim, optim_config, loss_fn)
		#np.random.seed(42)
		
		
	def addlayer(self, activation, units):
		self.net.addgate(activation, units)

	def train(self, X, Y):
		if X.ndim==1:			#####TODO checkdim func
			X = np.reshape(X,(1,len(X)))
			Y = np.reshape(Y,(1,len(Y)))
		Y_pred = self.net.forward(X)
		loss_value = self.net.backward(Y)
		self.net.update()
		return loss_value

	def predict(self, X):
		predicted_value = self.net.forward(X)
		return predicted_value


class Graph:

	# Computational graph class
	def __init__(self, input_dim, optim_config, loss_fn):
		self.id = input_dim
		self.optimizer = optim_config
		self.lf = loss_fn
		self.eta = 1
		self.layers = []
		self.current_layer_size = input_dim
		self.output = []
	

	def addgate(self, activation, units=0):

		if activation=='Linear':
			layer=Linear(self.current_layer_size+1,units)
			self.layers.append(layer)
			self.current_layer_size=units

		elif activation=='ReLU':
			layer=Linear(self.current_layer_size+1,units)
			self.layers.append(layer)
			layer=Relu()
			self.layers.append(layer)
			self.current_layer_size=units
	
		elif activation=='Sigmoid':
			layer=Linear(self.current_layer_size+1,units)
			self.layers.append(layer)
			layer=Sigmoid()
			self.layers.append(layer)
			self.current_layer_size=units
	
		elif activation=='Softmax':
			layer=Softmax()
			self.layers.append(layer)
			self.current_layer_size=units
	
		else:
			print "Invalid Gate ID!!"
		


	def forward(self, inp):
		predicted_value=np.array([])
		for i in xrange(len(self.layers)):
			predicted_value=self.layers[i].forward(inp)
			inp=predicted_value
		
		self.output=predicted_value
		return predicted_value



	def backward(self, expected):
		delta=np.array([])
		if self.lf=='L1':
			loss=L1_loss()
			delta=loss.backward(expected,self.output)

		elif self.lf=='L2':
			loss=L2_loss()
			#print loss.forward(expected,self.output)
			delta=loss.backward(expected,self.output)
			
		elif self.lf=='Cross_Entropy':
			loss=Cross_Entropy()
			print loss.forward(expected,self.output)," : e.f."
			delta=loss.backward(expected,self.output)
			#print delta,"ddeeellllllllll"
		
		elif self.lf=='SVM':			
			loss=SVM_loss(1)
			print loss.forward(expected,self.output)," : e.f."
			delta=loss.backward(expected)

		else:
			print "Invalid Loss Function ID!!"
		
		loss_val=np.array([])
		linear_not_found=True
		for i in reversed(xrange(len(self.layers))):
			loss_val=self.layers[i].backward(delta,linear_not_found)
			delta=loss_val
			if  isinstance(self.layers[i], Linear):
				linear_not_found=False

		return loss_val



	def update(self):
		for i in xrange(len(self.layers)):
			if  isinstance(self.layers[i], Linear):
				self.layers[i].w=(self.layers[i].w)+self.optimizer.weight_update(self.layers[i].input, self.layers[i].delta)


class Optimizer:
	def __init__(self, learning_rate, momentum_eta = 0.0):
		self.lr=learning_rate
		self.eta=momentum_eta
		self.prev_delta_w=0

	def weight_update(self, prev_output, next_delta):
		dataset_size=len(next_delta)
		curr_delta_w=self.lr*np.dot(prev_output.T,next_delta)/dataset_size
		result_delta_w=curr_delta_w+(self.eta*self.prev_delta_w)
		self.prev_delta_w=curr_delta_w
		return result_delta_w


class ReLU:
	# Example class for the ReLU layer. Replicate for other activation types and/or loss functions.


	def __init__(self):
		self.input=np.array([])
		
	def forward(self, inp):
		self.input=inp
		return np.maximum(0,inp)
		
	def backward(self, dz):
		return  1.*((self.input)>0)*dz




class Softmax:
	# Example class for the ReLU layer. Replicate for other activation types and/or loss functions.
	def __init__(self):
		self.tr_siz=0
		self.output=np.array([])

	def forward(self, input):
		self.tr_siz=len(input[0])
		s=np.sum(np.exp(input),axis=1)
		#print s,"futfiyf"
		#print np.exp(input),"etbb"
		self.output = np.exp(input)/np.reshape(s,(len(s),1))
		return self.output

	def backward(self, dz, last):
		der=np.empty((len(self.output),len(self.output[0]),len(self.output[0])))
		for k in xrange(len(self.output)):
			for i in xrange(len(self.output[0])):
				for j in xrange(len(self.output[0])):
					der[k][i][j]=self.output[k][i]*(self.kronecker_delta(i, j)-self.output[k][j])
		
		#print der,"derrrrrrrrrr"
		res=[]
		for k in xrange(len(self.output)):
			q=np.dot(der[k],dz[k].T)
			#print q,"qqqqqqqqq"
			res.append(q)
		#print np.array(res),"ressssssssssssssss"
		return np.array(res)

	def kronecker_delta(self, i, j):
		return int(i==j) 

class Sigmoid:
	# Example class for the ReLU layer. Replicate for other activation types and/or loss functions.
	def __init__(self):
		self.output=np.array([])

	def forward(self, inp):
		res=1/(1+np.exp(-inp))
		self.output=res        
		return res

	def backward(self, dz,last):
		s = self.output
		if last==False:
			s=np.insert(s,0,1,axis=1)
		return dz * s * (1-s)

class Linear:
	# Example class for the ReLU layer. Replicate for other activation types and/or loss functions.
	def __init__(self, d, m):
		self.w = 2*np.random.random((d,m)) - 1
		self.delta=np.array([])
		self.input=np.array([])

	def forward(self, input):
		input_with_bias=np.insert(input,0,1,axis=1)
		self.input=input_with_bias
		return np.dot(input_with_bias,self.w)

	def backward(self, dz, last):
	
		if last==False:
			self.delta=dz[:,1:]
			return np.dot(dz[:,1:],self.w.T)
		else: 
			self.delta=dz
			return np.dot(dz,self.w.T)

class L1_loss:
	# Example class for the ReLU layer. Replicate for other activation types and/or loss functions.
	def __init__(self):
		pass

	def forward(self, yd, yp):
		return np.sum(abs(np.mean((yd-yp),axis=1)))

	def backward(self, yd, yp):	
		return -np.nan_to_num(abs(yd-yp)/(yd-yp))


class L2_loss:
	# Example class for the ReLU layer. Replicate for other activation types and/or loss functions.
	def __init__(self):
		pass

	def forward(self, yd, yp):
		#print ((np.sum(np.mean(yd-yp)))**2)/2
		return ((np.sum(np.mean(yd-yp)))**2)/2
	def backward(self, yd, yp):
		#print np.shape(yd)," ",np.shape(yp)
		return yd-yp


class Cross_Entropy:
	# Example class for the ReLU layer. Replicate for other activation types and/or loss functions.
	def __init__(self):
		pass

	def forward(self, yd, yp):
		#print yd,"lllllllllllll"
		#print yp,"yyyiiipppiiiiieeeeeeeeee"
		#print yp-yd,"lossssssssssssssssss"
		return  np.average(-np.sum(yd*np.log(yp),axis=1))#-(np.sum(yd*np.log(yp)+(1-yd)*np.log(1-yp)))/len(yd)

	def backward(self, yd, yp):
		#print yp," ",yd," ",yp*(1-yp)
		return yd/yp#(yd-yp)/(yp*(1-yp))

class SVM_loss:
	# Example class for the ReLU layer. Replicate for other activation types and/or loss functions.
	def __init__(self,m):
		self.margin=m
		self.current_loss=[]

	def forward(self, yd, yp):
		class_index=np.where(yd==1)[1]
		#print class_index
		loss=[]
		
		for i in xrange(len(class_index)):
			#print class_index[i]
			mask=np.ones(len(yd[0]))
			mask[class_index[i]]=0
			'''
			print mask,"mmmmmmmmmm"		
			print yp,"yppppppppp"
			print yp[i][class_index[i]]
			print np.maximum(0,yp-yp[i][class_index[i]]+self.margin),"qqqqqqqqqqqq"	
			'''
			current=np.maximum(0,yp[i]-yp[i][class_index[i]]+self.margin)*mask
			loss.append(current)
		self.current_loss=loss
		#print np.sum(self.current_loss,axis=1),"looosssssss"
		'''
		print loss[0],"loss"
		'''
		final_loss=np.sum(self.current_loss,axis=1)
		#print ,"ooooooooooo"
		
		return np.mean(final_loss)	
		
	def backward(self, yd):
		class_index=np.where(yd==1)[1]
		#print class_index
		grad=np.zeros((len(yd),len(yd[0])))
		#print grad," gggg",self.current_loss
		for i in xrange(len(yd)):
			for j in xrange(len(yd[0])):
				if  j==class_index[i]:
					grad[i][j]=-np.sum(1.*(self.current_loss[i]>0))
					#print self.current_loss[i]," ccccccccccc"
				else:
					grad[i][j]=1.*(self.current_loss[i][j]>0)
		#print grad,"gradddddddddddddd"
		return -grad

if __name__ == "__main__":
	"""
	s=SVM_loss(10)
	print s.forward(np.array([[1,0,0]]),np.array([[13,-7,11]]))
	print s.backward(np.array([[1,0,0]]))
'''"""
	opti=Optimizer(0.1,0)
	nn_model = DenseNet(2,opti,"SVM")
	#nn_model.addlayer('Sigmoid',4)
	nn_model.addlayer('Linear',3)
	x = np.array([  [0,1],
					[1,0],
					[1,1],
					[0,0]  ])

	y = np.array([  [1,0],
					[1,0],
					[0,1],
					[0,1]  ])


	c=np.array([[2,5,3]])
	#error=np.random.uniform(-1,1,[60,1])	
	
	X=np.random.uniform(-1,1,[60,2])
	Xi=np.insert(X,0,1,axis=1)
	Y=np.dot(Xi,c.T) 	  ### y=c0+5*x1+3*x2+error

	t=np.random.uniform(-1,1,[60,2])
	ti=np.insert(t,0,1,axis=1)
	tY=np.dot(ti,c.T)

	
	x=np.array([[0.50,0.40],[0.80,0.30],[0.30,0.80],[-0.40,0.30],[-0.30,0.70],[-0.70,0.20],[0.70,-0.40],[0.50,-0.60],[-0.40,-0.50]])
	y=np.array([[1,0,0],[1,0,0],[1,0,0],[0,1,0],[0,1,0],[0,1,0],[0,0,1],[0,0,1],[0,0,1]])
	#print np.shape(Xi)," ",np.shape(Y)
	

	for i in xrange(50):
		#for j in xrange(4):
			nn_model.train(x,y)
		
	
	x=np.array([  [0,0],[1,0],[1,1],[0,1] ])
	x=np.array([[0.50,0.40],[-0.40,0.30],[-0.30,0.70],[-0.70,0.20],[0.70,-0.40],[0.50,-0.60],[-0.40,-0.50],[0.80,0.30],[0.30,0.80]])
	p=nn_model.predict(x)
	print "pred : ",p

	
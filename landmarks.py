'''
A face gesture(yaw roll pitch) regression by landmarks data using TF
Date: 2016/12/22
Ref: https://github.com/aymericdamien/TensorFlow-Examples/blob/master/notebooks/3_NeuralNetworks/multilayer_perceptron.ipynb 
'''
import tensorflow as tf
import numpy as np

# Parameters
learning_rate=0.03
training_epoches=10000
display_step=500

# Training Data
X_train=np.loadtxt("generated_landmarks/landmarks_9_11250_3.txt")
Y_train=np.loadtxt("generated_landmarks/rotation_param_9_11250_3.txt")
X_test=np.loadtxt("generated_landmarks/landmarks_9_test.txt")
Y_test=np.loadtxt("generated_landmarks/rotation_param_9_test.txt")
num_examples=X_train.shape[0]

# Network Params
n_input=18 # 9 points landmarks
n_hidden_1=256
n_hidden_2=256
n_output= 3 # 3 rotation param

# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_output])


# Create model
def multilayer_perceptron(x,weight,biases):
	# Hidden layer 
	layer_1=tf.add(tf.matmul(x,weights['h1']),biases['b1'])
	layer_1=tf.nn.sigmoid(layer_1)
	# Hidden layer 
	layer_2=tf.add(tf.matmul(layer_1,weights['h2']),biases['b2'])
	layer_1=tf.nn.sigmoid(layer_2)
	# output layer
	out_layer=tf.matmul(layer_2,weights['out'])+biases['out']
	return out_layer

# Store layers weight & bias
weights={
	'h1': tf.Variable(tf.random_normal([n_input,n_hidden_1])),
	'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
	'out': tf.Variable(tf.random_normal([n_hidden_2, n_output]))
}
biases = {
	'b1': tf.Variable(tf.random_normal([n_hidden_1])),
	'b2': tf.Variable(tf.random_normal([n_hidden_2])),
	'out': tf.Variable(tf.random_normal([n_output]))
}

# Construct model
pred=multilayer_perceptron(x,weights,biases)

# Define loss and optimizer
# mean squared error
#cost=tf.reduce_sum(tf.pow(pred-y,2))/num_examples
#cost=tf.reduce_sum(tf.square(tf.sub(pred,y)),1)
cost=tf.nn.l2_loss(pred-y)
#cost=tf.reduce_mean(tf.square(pred-y),1)
optimizer=tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
#optimizer=tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init=tf.initialize_all_variables()

# Launch the graph
with tf.Session() as sess:
	sess.run(init)

	# Training cycle
	for epoch in range(training_epoches):
		avg_cost=0.
		#total_batch=int(num_examples/batch_size)
		total_batch=1
		# Loop over all batches
		for i in range(total_batch):
			#batch_x,batch_y=X_train[i*batch_size:(i+1)*batch_size],Y_train[i*batch_size:(i+1)*batch_size]
			batch_x,batch_y=X_train,Y_train
			# Run optimization op (backprop) and cost op (to get loss value)
			_,c=sess.run([optimizer,cost],feed_dict={x:batch_x,y:batch_y})

			# Comput average loss
			avg_cost +=np.sum(c/total_batch)
		# Display logs per epoch step
		if epoch % display_step==0:
			print "Epoch:",'%04d'%(epoch+1),"cost=","{:.9f}".format(avg_cost)
	print "Optimization Finished!"

	# Test model
	# Calculate accuracy
	#accuracy=tf.reduce_mean(tf.square(tf.sub(pred,y)))
	#print "Accuracy:",accuracy.eval({x:X_test,y:Y_test})
	d=5
	print '---------------training data----------------'
	pd=pred.eval({x:X_train[:d,:]})
	print Y_train[:d,:]
	print '----------------'
	print pd[:d,:]
	print np.mean((pd-Y_train[:d,:])**2)

	print '----------------test data---------------'
	pd=pred.eval({x:X_test[:d,:]})
	print Y_test[:d,:]
	print '----------------'
	print pd[:d,:]
	print np.mean((pd-Y_test[:d,:])**2)
	
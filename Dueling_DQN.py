import tensorflow as tf
import numpy as np
import random

class DQN():

    def __init__(self):

        self.save_file = 'model/model.ckpt'

        self.img_size = 80
        self.Num_colorChannel = 1
        self.Num_action = 3
        self.Num_stacking = 4

        self.first_conv = [8,8,self.Num_colorChannel * self.Num_stacking, 32]
        self.second_conv = [4,4,32,64]
        self.third_conv = [3,3,64,64]
        self.first_dense = [10*10*64, 512]
        self.second_dense = [512, self.Num_action]

        self.first_epsilon = 1
        self.epsilon = self.first_epsilon
        self.final_epsilon = 0.1

        self.Num_batch = 32

        self.gamma = 0.99
        self.learning_rate = 0.00025

        # 얼마나 GPU 쓸 건지지
        self.GPU_fraction = 0.5

        self.Num_target_update = 5000

        #init network
        self.input, self.output = self.network('network')
        self.input_target, self.output_target = self.network('target')
        self.train_step, self.action_target, self.y_target = self.loss_and_train()
        self.sess = self.init_sess()


    def update_target(self):

        trainable_val = tf.trainable_variables()

        #network_vals
        trainable_val_network = [var for var in trainable_val if var.name.startswith('network')]

        #target_vals
        trainable_val_target = [var for var in trainable_val if var.name.startswith('target')]

        for i in range(len(trainable_val_network)):
            self.sess.run(tf.assign(trainable_val_target[i], trainable_val_network[i]))

    def train(self, replay_memory):

        minibatch = random.sample(replay_memory, self.Num_batch)

        # Save the each batch data
        state_batch = [batch[0] for batch in minibatch]
        action_batch = [batch[1] for batch in minibatch]
        reward_batch = [batch[2] for batch in minibatch]
        next_state_batch = [batch[3] for batch in minibatch]
        terminal_batch = [batch[4] for batch in minibatch]
        
        # target값 저장할 리스트
        y_batch = []

        #target network 로 추측
        Q_batch = self.output_target.eval(feed_dict={self.input_target: next_state_batch})


        for i in range(len(minibatch)):
            if terminal_batch[i] == True:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + self.gamma*np.max(Q_batch[i]))


        self.train_step.run(feed_dict={
            self.action_target: action_batch,
            self.y_target: y_batch,
            self.input: state_batch})

    def loss_and_train(self):

        action_target = tf.placeholder(tf.float32, shape=[None, self.Num_action])
        # 계산된 타겟
        y_target = tf.placeholder(tf.float32, shape=[None])

        y_prediction = tf.reduce_sum(tf.multiply(self.output, action_target), reduction_indices=1)

        # loss : (Target - Q)^2
        loss = tf.reduce_mean(tf.square(y_prediction - y_target))
        train_step = tf.train.AdamOptimizer(learning_rate=self.learning_rate, epsilon=1e-02).minimize(loss)

        return train_step, action_target, y_target

    def select_action(self, stacked_state):
        action = np.zeros([self.Num_action])
        action_index = 0

        #choose action
        if random.random() < self.epsilon:
            action_index = random.randint(0, self.Num_action - 1)
            action[action_index] = 1
        else:
            # 화면을 대입해 Q_value 도출
            Q_value = self.output.eval(feed_dict={self.input: [stacked_state]})
            action_index = np.argmax(Q_value)
            action[action_index] = 1

        #epsilon process
        if self.epsilon > self.final_epsilon:
            self.epsilon -= self.epsilon / 100000
        else:
            self.epsilon = self.final_epsilon

        return action

    def select_action_testing(self, state):
        action = np.zeros([self.Num_action])

        # 화면을 대입해 Q_value 도출
        Q_value = self.output.eval(feed_dict={self.input: [state]})
        action_index = np.argmax(Q_value)
        action[action_index] = 1

        self.epsilon = 0

        return action


    def init_sess(self):

        config = tf.ConfigProto()
        config.gpu_options.per_process_gpu_memory_fraction = self.GPU_fraction

        sess = tf.InteractiveSession(config=config)
        init = tf.global_variables_initializer()
        sess.run(init)

        return sess


    def conv2d(self, x, w, stride):
        return tf.nn.conv2d(x, w, strides=[1, stride, stride, 1], padding='SAME')

    def conv_weight_variable(self, name, shape):
        return tf.get_variable(name, shape=shape, initializer=tf.contrib.layers.xavier_initializer_conv2d())

    def weight_variable(self, name, shape):
        return tf.get_variable(name, shape=shape, initializer=tf.contrib.layers.xavier_initializer())

    def bias_variable(self, name, shape):
        return tf.get_variable(name, shape=shape, initializer=tf.contrib.layers.xavier_initializer())

    def network(self, network_name):


        x_image = tf.placeholder(tf.float32,
                                 shape=[None, self.img_size, self.img_size, self.Num_colorChannel * self.Num_stacking])
        x_normalize = (x_image - (255.0/2)) / (255.0/2)

        with tf.variable_scope(network_name):
            #conv variables
            w_conv1 = self.conv_weight_variable('w_conv1', self.first_conv) #[8,8,1,32]
            b_conv1 = self.bias_variable('b_conv1', [self.first_conv[3]]) #[32]

            w_conv2 = self.conv_weight_variable('w_conv2', self.second_conv) #[4,4,32,64]
            b_conv2 = self.bias_variable('b_conv2', [self.second_conv[3]]) #[64]

            w_conv3 = self.conv_weight_variable('w_conv3', self.third_conv) #[3,3,64,64]
            b_conv3 = self.bias_variable('b_conv3', [self.third_conv[3]]) #[64]

            # first_dense
            w_fc1 = self.weight_variable('w_fc1', self.first_dense)
            b_fc1 = self.bias_variable('b_fc1', [self.first_dense[1]])

            w_fc2 = self.weight_variable('w_fc2', self.second_dense)
            b_fc2 = self.bias_variable('b_fc2', [self.second_dense[1]])

            #fully connected layer action
            w_fc_A = self.weight_variable('w_fc1_A', [512, 3])
            b_fc_A = self.bias_variable('b_fc1_A', [3])

            #fully connected layer value
            w_fc_V = self.weight_variable('w_fc2_V', [512, 1])
            b_fc_V = self.bias_variable('b_fc2_V', [1])

        #network
        #output size: (the size of image - that of filter) / stride + 1
        #(80 - 32) / 4 + 1 =
        h_conv1 = tf.nn.relu(self.conv2d(x_normalize, w_conv1, 4) + b_conv1)
        h_conv2 = tf.nn.relu(self.conv2d(h_conv1, w_conv2, 2) + b_conv2)
        h_conv3 = tf.nn.relu(self.conv2d(h_conv2, w_conv3, 1) + b_conv3)


        #flatten
        h_flat = tf.reshape(h_conv3, [-1, self.first_dense[0]])

        h_fc1 = tf.nn.relu(tf.matmul(h_flat, w_fc1) + b_fc1)


        #A
        output_A = tf.matmul(h_fc1, w_fc_A) + b_fc_A

        #V
        output_V = tf.matmul(h_fc1, w_fc_V) + b_fc_V

        
        # 계산
        # output = value + (advantage - mean(advantage))
        output = output_V + tf.subtract(output_A, tf.reduce_mean(output_A))

        return x_image, output









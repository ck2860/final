import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import tensorflow.compat.v1 as tf
from ContextualBandit import *
from ContextualBanditAgent import *
# warnings.filterwarnings('ignore', category=FutureWarning)
# warnings.filterwarnings('ignore', category=DeprecationWarning)
# tf.logging.set_verbosity(tf.logging.ERROR)

## Documentation for Greedy Strategies class
# this class has decreasing-epsilon, greedy-epsilon, hybrid#1, hybrid#2, hybrid#3, hybrid#4, and hybrid#5 functions.
# ContextualBandit and ContextualBanditAgent classes are used here. Please go to see Class tab for more details.


class Greedystrategies():
    def __init__(self, n):
        self.numberOfTrials = n

    ## Documentation for Decreasing Epsilon function
    # this would return the rewards of Decreasing Epsilon
    ##@param a1: random seed
    ##@param df1a: initialized dataframe
    def decreasingEpsilon(self, a1, df1a):
        for a in range(self.numberOfTrials):
            tf.reset_default_graph()
            cBandit = contextual_bandit()
            myAgent = agent(lr=0.005, s_size=cBandit.num_bandits, a_size=cBandit.num_actions)
            weights = tf.trainable_variables()[0]   # The weights we will evaluate to look into the network.
            total_episodes = 10000  # Set total number of episodes to train agent on.
            total_reward = np.zeros([cBandit.num_bandits, cBandit.num_actions])  # Set scoreboard for bandits to 0.
            e = 1  # start with highly explorative (100% explore, 0% exploit)
            init = tf.global_variables_initializer()

            # Launch the tensorflow graph
            with tf.Session() as sess:
                sess.run(init)
                i = 0
                np.random.seed(a1)
                while i < total_episodes:
                    s = cBandit.getBandit()  # Get a state from the environment.
                    # Choose either a random action or one from our network.
                    r = np.random.rand(1)
                    if r < e:
                        action = np.random.randint(cBandit.num_actions)  # explore
                    else:
                        action = sess.run(myAgent.chosen_action, feed_dict={myAgent.state_in: [s]})  # exploit
                    reward = cBandit.pullArm(action)  # Get our reward for taking an action given a bandit.

                    # Update the network.
                    feed_dict = {myAgent.reward_holder: [reward], myAgent.action_holder: [action], myAgent.state_in: [s]}
                    _, ww = sess.run([myAgent.update, weights], feed_dict=feed_dict)

                    # Update our running tally of scores.
                    total_reward[s, action] += reward
                    if i % 500 == 0:
                        meanR = np.mean(total_reward, axis=1)
                        df1a = df1a.append({'x': i, 'y': meanR[0]}, ignore_index=True)
                        # print("Epsilon-Decreasing mean rewards: " + str(meanR[0]) + " at the episode of " + str(i))
                    e -= 0.0001  # in the end it would be highly exploitative
                    i += 1
                a1 += 1
                print("Trial#", a+1, ": Epsilon-Decreasing is done! ")
        return df1a

    ## Documentation for Epsilon-Greedy function
    # this would return the rewards of Epsilon-Greedy
    ##@param b: random seed
    ##@param df2a: initialized dataframe
    def EpsilonGreedy(self, b, df2a):
        for a in range(self.numberOfTrials):
            tf.reset_default_graph()
            cBandit = contextual_bandit()
            myAgent = agent(lr=0.005, s_size=cBandit.num_bandits, a_size=cBandit.num_actions)
            weights = tf.trainable_variables()[0]  # The weights we will evaluate to look into the network.
            total_episodes = 10000  # Set total number of episodes to train agent on.
            total_reward = np.zeros([cBandit.num_bandits, cBandit.num_actions])  # Set scoreboard for bandits to 0.
            # this is the probability of the agent to explore. 10% to explore and 90% of exploit
            e = 0.1
            init = tf.global_variables_initializer()
            # Launch the tensorflow graph
            with tf.Session() as sess:
                sess.run(init)
                i = 0
                np.random.seed(b)
                while i < total_episodes:
                    s = cBandit.getBandit()  # Get a state from the environment.
                    # Choose either a random action or one from our network.
                    r = np.random.rand(1)
                    if r < e:
                        action = np.random.randint(cBandit.num_actions) # explore
                    else:
                        action = sess.run(myAgent.chosen_action, feed_dict={myAgent.state_in: [s]})  # exploit

                    reward = cBandit.pullArm(action)  # Get our reward for taking an action given a bandit.
                    # Update the network.
                    feed_dict = {myAgent.reward_holder: [reward], myAgent.action_holder: [action], myAgent.state_in: [s]}
                    _, ww = sess.run([myAgent.update, weights], feed_dict=feed_dict)
                    # Update our running tally of scores.
                    total_reward[s, action] += reward
                    if i % 500 == 0:
                        meanR = np.mean(total_reward, axis=1)
                        df2a = df2a.append({'x': i, 'y': meanR[0]}, ignore_index=True)
                        # print("Epsilon-Greedy mean rewards: " + str(meanR[0]) + " at the episode of " + str(i))
                    i += 1
                b += 1
                print("Trial#", a+1, ": Epsilon-Greedy is done!")
        return df2a

    ## Documentation for Hybrid #1 function
    # this would return the rewards of Hybrid #1
    ##@param c: random seed
    ##@param df3a: initialized dataframe
    def hybrid1(self, c, df3a):
        for a in range(self.numberOfTrials):
            # hybrid #1
            tf.reset_default_graph()
            cBandit = contextual_bandit()
            myAgent = agent(lr=0.005, s_size=cBandit.num_bandits, a_size=cBandit.num_actions)
            weights = tf.trainable_variables()[0]  # The weights we will evaluate to look into the network.
            total_episodes = 10000  # Set total number of episodes to train agent on.
            total_reward = np.zeros([cBandit.num_bandits, cBandit.num_actions])  # Set scoreboard for bandits to 0.
            e = 0.9  # start with highly explorative (90% explore, 10% exploit)
            init = tf.global_variables_initializer()
            # Launch the tensorflow graph
            with tf.Session() as sess:
                sess.run(init)
                i = 0
                np.random.seed(c)
                while i < total_episodes:
                    s = cBandit.getBandit()  # Get a state from the environment.
                    # Choose either a random action or one from our network.
                    r = np.random.rand(1)
                    if r < e:
                        action = np.random.randint(cBandit.num_actions)  # explore
                    else:
                        action = sess.run(myAgent.chosen_action, feed_dict={myAgent.state_in: [s]})  # exploit
                    reward = cBandit.pullArm(action)  # Get our reward for taking an action given a bandit.
                    # Update the network.
                    feed_dict = {myAgent.reward_holder: [reward], myAgent.action_holder: [action], myAgent.state_in: [s]}
                    _, ww = sess.run([myAgent.update, weights], feed_dict=feed_dict)

                    # Update our running tally of scores.
                    total_reward[s, action] += reward
                    if i % 500 == 0:
                        meanR = np.mean(total_reward, axis=1)
                        df3a = df3a.append({'x': i, 'y': meanR[0]}, ignore_index=True)
                        # print("Hybrid#1 mean rewards: " + str(meanR[0]) + " at the episode of " + str(i))
                    e -= 0.00008  # in the end it would be highly exploitative (10% explore, 90% exploit)
                    i += 1
                c += 1
                print("Trial#", a+1, ": Hybrid#1 is done!")
        return df3a

    ## Documentation for Hybrid #2 function
    # this would return the rewards of Hybrid #2
    ##@param d: random seed
    ##@param df4a: initialized dataframe
    def hybrid2(self, d, df4a):
        for a in range(self.numberOfTrials):
            tf.reset_default_graph()
            cBandit = contextual_bandit()
            myAgent = agent(lr=0.005, s_size=cBandit.num_bandits, a_size=cBandit.num_actions)
            weights = tf.trainable_variables()[0] #The weights we will evaluate to look into the network.
            total_episodes = 10000 #Set total number of episodes to train agent on.
            total_reward = np.zeros([cBandit.num_bandits, cBandit.num_actions]) #Set scoreboard for bandits to 0.
            e = 1 #start with highly explorative (90% explore, 10% exploit)
            init = tf.global_variables_initializer()
            # Launch the tensorflow graph
            with tf.Session() as sess:
                sess.run(init)
                i = 0
                np.random.seed(d)
                while i < total_episodes:
                    s = cBandit.getBandit()  # Get a state from the environment.

                    # Choose either a random action or one from our network.
                    r = np.random.rand(1)
                    if r < e:
                        action = np.random.randint(cBandit.num_actions)  # explore
                    else:
                        action = sess.run(myAgent.chosen_action, feed_dict={myAgent.state_in: [s]})  # exploit
                    reward = cBandit.pullArm(action)  # Get our reward for taking an action given a bandit.

                    # Update the network.
                    feed_dict = {myAgent.reward_holder: [reward], myAgent.action_holder: [action], myAgent.state_in: [s]}
                    _, ww = sess.run([myAgent.update, weights], feed_dict=feed_dict)

                    # Update our running tally of scores.
                    total_reward[s, action] += reward
                    if i % 500 == 0:

                        meanR = np.mean(total_reward, axis=1)
                        df4a = df4a.append({'x': i, 'y': meanR[0]}, ignore_index=True)
                        # print("Hybrid#2 mean rewards: " + str(meanR[0]) + " at the episode of "+ str(i))
                    e -= 0.00018  # in the end it would be highly exploitative (10% explore, 90% exploit)
                    if e < 0.1:
                        e = 0.1
                    i += 1
                d += 1
                print("Trial#", a+1, ": Hybrid#2 is done!")
        return df4a

    ## Documentation for Hybrid #3 function
    # this would return the rewards of Hybrid #3
    ##@param e1: random seed
    ##@param df5a: initialized dataframe
    def hybrid3(self, e1, df5a):
        for a in range(self.numberOfTrials):
            # Hybrid#3
            tf.reset_default_graph()
            cBandit = contextual_bandit()
            myAgent = agent(lr=0.005, s_size=cBandit.num_bandits, a_size=cBandit.num_actions)
            weights = tf.trainable_variables()[0]  # The weights we will evaluate to look into the network.
            total_episodes = 10000  # Set total number of episodes to train agent on.
            total_reward = np.zeros([cBandit.num_bandits, cBandit.num_actions])  # Set scoreboard for bandits to 0.
            e = 0.9  # start with highly explorative (90% explore, 10% exploit)

            init = tf.global_variables_initializer()

            # Launch the tensorflow graph
            with tf.Session() as sess:
                sess.run(init)
                i = 0
                np.random.seed(e1)
                while i < total_episodes:
                    s = cBandit.getBandit()  # Get a state from the environment.

                    # Choose either a random action or one from our network.
                    r = np.random.rand(1)
                    if r < e:
                        action = np.random.randint(cBandit.num_actions)  # explore
                    else:
                        action = sess.run(myAgent.chosen_action, feed_dict={myAgent.state_in: [s]})  # exploit

                    reward = cBandit.pullArm(action)  # Get our reward for taking an action given a bandit.

                    # Update the network.
                    feed_dict = {myAgent.reward_holder: [reward], myAgent.action_holder: [action], myAgent.state_in: [s]}
                    _, ww = sess.run([myAgent.update, weights], feed_dict=feed_dict)

                    # Update our running tally of scores.
                    total_reward[s, action] += reward
                    if i % 500 == 0:

                        meanR = np.mean(total_reward, axis=1)
                        df5a = df5a.append({'x': i, 'y': meanR[0]}, ignore_index=True)
                        # print("Hybrid#3 mean rewards: " + str(meanR[0]) + " at the episode of " + str(i))
                    e -= 0.00016  # in the end it would be highly exploitative (10% explore, 90% exploit)
                    if e < 0.1:
                        e = 0.1
                    i += 1
                e1 += 1
                print("Trial#", a+1, ": Hybrid#3 is done!")
        return df5a

    ## Documentation for Hybrid #4 function
    # this would return the rewards of Hybrid #4
    ##@param f: random seed
    ##@param df6a: initialized dataframe
    def hybrid4(self, f, df6a):
        for a in range(self.numberOfTrials):
            #Hybrid#4
            tf.reset_default_graph()
            cBandit = contextual_bandit()
            myAgent = agent(lr=0.005, s_size=cBandit.num_bandits, a_size=cBandit.num_actions)
            weights = tf.trainable_variables()[0]  # The weights we will evaluate to look into the network.
            total_episodes = 10000  # Set total number of episodes to train agent on.
            total_reward = np.zeros([cBandit.num_bandits, cBandit.num_actions])  # Set scoreboard for bandits to 0.
            e = 1  # start with highly explorative (90% explore, 10% exploit)

            init = tf.global_variables_initializer()
            # Launch the tensorflow graph
            with tf.Session() as sess:
                sess.run(init)
                i = 0
                np.random.seed(f)
                while i < total_episodes:
                    s = cBandit.getBandit()  # Get a state from the environment.
                    # Choose either a random action or one from our network.
                    r = np.random.rand(1)
                    if r < e:
                        action = np.random.randint(cBandit.num_actions)  # explore
                    else:
                        action = sess.run(myAgent.chosen_action, feed_dict={myAgent.state_in: [s]})  # exploit
                    reward = cBandit.pullArm(action)  # Get our reward for taking an action given a bandit.

                    # Update the network.
                    feed_dict = {myAgent.reward_holder: [reward], myAgent.action_holder: [action], myAgent.state_in: [s]}
                    _, ww = sess.run([myAgent.update, weights], feed_dict=feed_dict)

                    # Update our running tally of scores.
                    total_reward[s, action] += reward
                    if i % 500 == 0:

                        meanR = np.mean(total_reward, axis=1)
                        df6a = df6a.append({'x': i, 'y': meanR[0]}, ignore_index=True)
                        # print("Hybrid#4 mean rewards: " + str(meanR[0]) + " at the episode of " + str(i))
                    e -= 0.00036  # in the end it would be highly exploitative (10% explore, 90% exploit)
                    if e < 0.1:
                        e = 0.1
                    i += 1
                f += 1
                print("Trial#", a+1, ": Hybrid#4 is done!")
        return df6a

    ## Documentation for Hybrid #5 function
    # this would return the rewards of Hybrid #5
    ##@param g: random seed
    ##@param df7a: initialized dataframe
    def hybrid5(self, g, df7a):
        for a in range(self.numberOfTrials):
            # Hybrid#5
            tf.reset_default_graph()
            cBandit = contextual_bandit()
            myAgent = agent(lr=0.005, s_size=cBandit.num_bandits, a_size=cBandit.num_actions)
            weights = tf.trainable_variables()[0]  # The weights we will evaluate to look into the network.
            total_episodes = 10000  # Set total number of episodes to train agent on.
            total_reward = np.zeros([cBandit.num_bandits, cBandit.num_actions])  # Set scoreboard for bandits to 0.
            e = 0.9  # start with highly explorative (90% explore, 10% exploit)

            init = tf.global_variables_initializer()

            # Launch the tensorflow graph
            with tf.Session() as sess:
                sess.run(init)
                i = 0
                np.random.seed(g)
                while i < total_episodes:
                    s = cBandit.getBandit()  # Get a state from the environment.

                    # Choose either a random action or one from our network.
                    r = np.random.rand(1)
                    if r < e:
                        action = np.random.randint(cBandit.num_actions)  #explore
                    else:
                        action = sess.run(myAgent.chosen_action, feed_dict={myAgent.state_in: [s]}) #exploit

                    reward = cBandit.pullArm(action)  # Get our reward for taking an action given a bandit.

                    # Update the network.
                    feed_dict = {myAgent.reward_holder: [reward], myAgent.action_holder: [action], myAgent.state_in: [s]}
                    _, ww = sess.run([myAgent.update, weights], feed_dict=feed_dict)

                    # Update our running tally of scores.
                    total_reward[s, action] += reward
                    if i % 500 == 0:

                        meanR = np.mean(total_reward, axis=1)
                        df7a = df7a.append({'x': i, 'y': meanR[0]}, ignore_index=True)
                        # print("Hybrid#5 mean rewards: " + str(meanR[0]) + " at the episode of " + str(i))
                    e -= 0.00032  # in the end it would be highly exploitative (10% explore, 90% exploit)
                    if e < 0.1:
                        e = 0.1
                    i += 1
                g += 1
                print("Trial#", a+1, ": Hybrid#5 is done!")
        return df7a

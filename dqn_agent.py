import time
import math
import random
import numpy as np
from collections import deque
from copy import deepcopy
import torch
import torch.optim as optim
from torch.autograd import Variable
import gym
import gym_airsim

from replay_memory import SequentialMemory
from agent import Agent
from schedule import LinearSchedule
import constants
import utils

dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

class DQNAgent(Agent):
    def __init__(self, placeRecognition=None, navigation=None, checkpoint_path="checkpoint", train_iter=1000, teach_commands_file=None):
        super(DQNAgent, self).__init__(placeRecognition, navigation)
        self.env = gym.make('AirSim-v1')
        self.env.reset()
        self.goal = None
        self.init = None
        self.teachCommandsFile = teach_commands_file
        self.path = []
        self.step = 0
        self.num_param_updates = 0
        self.checkpoint_path = checkpoint_path
        self.train_iter = train_iter
        self.target_navigation = deepcopy(navigation)
        self.exploration_schedule = LinearSchedule(100000, 0.1)
        self.optimizer = optim.RMSprop(list(filter(lambda p: p.requires_grad, self.navigation.model.parameters())), lr=constants.DQN_LEARNING_RATE)

        utils.hard_update(self.navigation.target_model, self.navigation.model)

        self.memory = SequentialMemory(limit=constants.DQN_MEMORY_SIZE, window_length=1)

    def random_walk(self):
        state = self.env.reset()
        self.init = state
        previous_action = -1
        for i in range(constants.DQN_LOCO_TEACH_LEN):
            action = random.randint(0, constants.LOCO_NUM_CLASSES-1)
            next_state, _, done, info = self.env.step(action)
            position = (info['x_pos'], info['y_pos'], info['z_pos'], info['yaw'])
            rep, _ = self.sptm.append_keyframe(state, action, done, position=position)
            self.path.append(position)
            self.goal = state
            state = next_state
            if done:
                break

    def random_consistent_walk(self):
        state = self.env.reset()
        self.init = state
        previous_action = -1
        for i in range(constants.DQN_LOCO_TEACH_LEN):
            actions = [i for i in range(0, constants.LOCO_NUM_CLASSES)]
            if (previous_action == 1):
                actions.remove(2)
            elif (previous_action == 2):
                actions.remove(1)
            elif (previous_action == 3):
                actions.remove(4)
            elif (previous_action == 4):
                actions.remove(3)
            action = random.choice(actions)
            print (actions, action)
            next_state, _, done, info = self.env.step(action)
            position = (info['x_pos'], info['y_pos'], info['z_pos'], info['yaw'])
            rep, _ = self.sptm.append_keyframe(state, action, done, position=position)
            self.path.append(position)
            self.goal = state
            state = next_state
            previous_action = action
            if done:
                break

    def random_consistent_walk(self):
        state = self.env.reset()
        self.init = state
        previous_action = -1
        for i in range(constants.DQN_LOCO_TEACH_LEN):
            actions = [i for i in range(0, constants.LOCO_NUM_CLASSES)]
            if (previous_action == 1):
                actions.remove(2)
            elif (previous_action == 2):
                actions.remove(1)
            elif (previous_action == 3):
                actions.remove(4)
            elif (previous_action == 4):
                actions.remove(3)
            action = random.choice(actions)
            print (actions, action)
            next_state, _, done, info = self.env.step(action)
            position = (info['x_pos'], info['y_pos'], info['z_pos'], info['yaw'])
            rep, _ = self.sptm.append_keyframe(state, action, done, position=position)
            self.path.append(position)
            self.goal = state
            state = next_state
            previous_action = action
            if done:
                break

    def consistent_walk(self):
        state = self.env.reset()
        self.init = state
        action = random.randint(0, constants.LOCO_NUM_CLASSES-1)
        for i in range(constants.DQN_LOCO_TEACH_NUM_CONSISTENT_ACTION):
            print (action)
            next_state, _, done, info = self.env.step(action)
            position = (info['x_pos'], info['y_pos'], info['z_pos'], info['yaw'])
            rep, _ = self.sptm.append_keyframe(state, action, done, position=position)
            self.path.append(position)
            self.goal = state
            state = next_state
            previous_action = action
            if done:
                break
        action = 0
        for i in range(constants.DQN_LOCO_TEACH_NUM_CONSISTENT_ACTION):
            print (action)
            next_state, _, done, info = self.env.step(action)
            position = (info['x_pos'], info['y_pos'], info['z_pos'], info['yaw'])
            rep, _ = self.sptm.append_keyframe(state, action, done, position=position)
            self.path.append(position)
            self.goal = state
            state = next_state
            previous_action = action
            if done:
                break

    def commanded_walk(self):
        action_file = open(self.teachCommandsFile)
        if action_file == None:
            return None

        state = self.env.reset()
        self.init = state
        i = 0
        actions = [int(val) for val in action_file.read().split('\n') if val.isdigit()]
        for action in actions:
            print ("commanded walk: index %d action %d" % (i, action))
            next_state, _, done, info = self.env.step(action)
            position = (info['x_pos'], info['y_pos'], info['z_pos'], info['yaw'])
            rep, _ = self.sptm.append_keyframe(state, action, done, position=position)
            self.path.append(position)
            self.goal = state
            state = next_state
            previous_action = action
            i = i+1
            if done:
                break

    def teach(self):
        if (self.teachCommandsFile == None):
            # self.random_walk()
            # self.random_consistent_walk()
            self.consistent_walk()
        else:
            self.commanded_walk()

    def select_epilson_greedy_action(self, observation):
        sample = random.random()
        eps_threshold = self.exploration_schedule.value(self.step)
        action = 0
        if sample > eps_threshold:
            actions = self.navigation.forward(*observation)
            prob, pred = torch.max(actions.data, 1)
            prob = prob.data.cpu().item()
            action = pred.data.cpu().item()

#            m = Categorical(actions)
#            action = m.sample()
            print ("network action selected")
        else:
            action = random.randint(0, constants.LOCO_NUM_CLASSES-1)
            print ("random action selected")
        return action

    def repeat(self):
        self.sptm.build_graph(with_shortcuts=False)
        goal, goal_index, similarity = self.sptm.find_closest(self.goal)
        if (goal_index < 0):
            print ("cannot find goal")
            return

        current_state = self.env.reset()
        previous_state = current_state
        info = self.env.get_position_orientation()
        position = (info['x_pos'], info['y_pos'], info['z_pos'], info['yaw'])
        episode_step = 0
        while (True):
            matched_index, similarity_score, best_velocity = self.sptm.relocalize(current_state)
#            matched_index, similarity_score, best_velocity = self.sptm.ground_relocalize(position)
#            matched_index, similarity_score, best_velocity = self.sptm.ground_lookahead_relocalize(position)

            matched_distance = self.calculate_distance(position, self.sptm.memory[matched_index].position)
            if (matched_distance > constants.DQN_MAX_DISTANCE_THRESHOLD):
                print ("Leaving the path, finishing episode")
                break

            path = self.sptm.find_shortest_path(matched_index, goal_index)
            print (matched_index, similarity_score, path)
            if (len(path) < 2): # achieved the goal
                return

            closest_state = self.sptm.memory[matched_index].state
            future_state = self.sptm.memory[path[1]].state
            if (self.step > constants.DQN_LEARNING_OFFSET_START):
                action = self.select_epilson_greedy_action((current_state, closest_state, future_state))
            else:
                action = random.randint(0, constants.LOCO_NUM_CLASSES-1)
            print ("action %d" % action)

            next_state, _, done, info = self.env.step(action)
            next_position = (info['x_pos'], info['y_pos'], info['z_pos'], info['yaw'])
            print ("positions: ", position, next_position, self.sptm.memory[path[1]].position)
            reward = self.compute_reward(position, next_position, path)
            print ("---> reward {}".format(reward))
            self.memory.append((current_state, closest_state, future_state), action, reward, False)
            previous_state = current_state.copy()
            current_state = next_state.copy()
            position = next_position
            if (done):
                break
            self.step = self.step + 1
            episode_step = episode_step + 1
            if (episode_step > constants.DQN_LOCO_TEACH_LEN * 3):
                break

    def compute_reward(self, previous_position, current_position, current_path):
        if (len(self.path) < 1):
            return 0
        # distances = [self.calculate_distance(current_position, position) for position in self.path]
        # distances.sort()
        # return distances[0]

        # distance = self.calculate_distance(current_position, self.sptm.memory[current_path[1]].position)
        # reward = (constants.DQN_REWARD_DISTANCE_OFFSET - distance)
        # return reward

        # angle = self.calculate_angle(current_position, self.sptm.memory[current_path[1]].position)
        # min_abs_angle = math.fabs(angle)
        # min_angle = angle
        # for i in range(1, len(current_path)):
        #     distance = self.calculate_distance(current_position, self.sptm.memory[current_path[i]].position)
        #     print ("distance to {}: {}".format(i, distance))
        #     if (distance < constants.DQN_MAX_DISTANCE_THRESHOLD):
        #         angle = self.calculate_angle(current_position, self.sptm.memory[current_path[i]].position)
        #         if (math.fabs(angle) < min_abs_angle):
        #             min_abs_angle = math.fabs(angle)
        #             min_angle = angle


        current_angle = self.calculate_angle(current_position, self.sptm.memory[current_path[1]].position)
        previous_angle = self.calculate_angle(previous_position, self.sptm.memory[current_path[1]].position)

        current_distance = self.calculate_distance(current_position, self.sptm.memory[current_path[1]].position)
        previous_distance = self.calculate_distance(previous_position, self.sptm.memory[current_path[1]].position)

        angle_reward = (math.fabs(previous_angle) - math.fabs(current_angle)) / (constants.AIRSIM_YAW_SPEED)
        angle_reward = np.clip(angle_reward, -1., 1.)
        distance_reward = (previous_distance - current_distance) / (constants.AIRSIM_STRAIGHT_SPEED)
        distance_reward = np.clip(distance_reward, -1., 1.)
        print ("current angle: {} - previous angle: {} - angle reward: {} || current distance: {} - previous distance: {} - distance reward: {}".format(current_angle, previous_angle, angle_reward, current_distance, previous_distance, distance_reward))
        reward = (distance_reward * constants.DQN_DISTANCE_REWARD_WEIGHT + angle_reward * constants.DQN_ANGLE_REWARD_WEIGHT) / (constants.DQN_DISTANCE_REWARD_WEIGHT + constants.DQN_ANGLE_REWARD_WEIGHT)
        return (reward)

    def calculate_angle(self, start_coordinates, current_coordinates):
        # abs_angle_difference = math.fabs(start_coordinates[3] - current_coordinates[3])
        # angle = min(abs_angle_difference, 360.0 - abs_angle_difference)

        angle_difference = math.fabs(current_coordinates[3] - start_coordinates[3])
        angle_difference_norm = min(angle_difference, math.pi - angle_difference)
        print ("angle diff: ", angle_difference_norm)
        heading_angle = math.fabs(math.atan2((current_coordinates[1] - start_coordinates[1]), (current_coordinates[0] - start_coordinates[0])) - start_coordinates[3])
        heading_angle_norm = min(heading_angle, math.pi - heading_angle)
        print ("heading diff: ", heading_angle_norm)
        angle = (angle_difference_norm + heading_angle_norm) / 2.
        angle_norm = min(angle, math.pi - angle)
        return angle_norm

    def calculate_distance(self, start_coordinates, current_coordinates):
        distance = math.sqrt((start_coordinates[0] - current_coordinates[0]) ** 2 +
                             (start_coordinates[1] - current_coordinates[1]) ** 2 + 
                             (start_coordinates[2] - current_coordinates[2]) ** 2)
        # abs_angle_difference = math.fabs(start_coordinates[3] - current_coordinates[3])
        # angle = min(abs_angle_difference, 360.0 - abs_angle_difference)
        return distance

    def update_policy(self):
        state0_batch = []
        state1_batch = []
        action_batch = []
        terminal1_batch = []
        reward_batch = []

        experiences = self.memory.sample(constants.DQN_BATCH_SIZE)
        for experience in experiences:
            current_state0 = self.navigation.np_preprocess(np.asarray(experience.state0[0][0]))
            closest_state0 = self.navigation.np_preprocess(np.asarray(experience.state0[0][1]))
            future_state0 = self.navigation.np_preprocess(np.asarray(experience.state0[0][2]))
            state0 = np.concatenate([current_state0, closest_state0, future_state0], axis=0)
            state0_batch.append(state0)

            current_state1 = self.navigation.np_preprocess(np.asarray(experience.state1[0][0]))
            closest_state1 = self.navigation.np_preprocess(np.asarray(experience.state1[0][1]))
            future_state1 = self.navigation.np_preprocess(np.asarray(experience.state1[0][2]))
            state1 = np.concatenate([current_state1, closest_state1, future_state1], axis=0)
            state1_batch.append(state1)

            action_batch.append(experience.action)
            terminal1_batch.append(0. if experience.terminal1 else 1.)
            reward_batch.append(experience.reward)

        state0_tensor = torch.from_numpy(np.asarray(state0_batch))# .float()
        state1_tensor = torch.from_numpy(np.asarray(state1_batch))# .float()
        action_tensor = torch.from_numpy(np.asarray(action_batch)).long()
        terminal1_tensor = torch.from_numpy(np.asarray(terminal1_batch)).float()
        reward_tensor = torch.from_numpy(np.asarray(reward_batch)).float()
        use_gpu = torch.cuda.is_available()
        if use_gpu:
            state0_variable, state1_variable, action_variable, terminal1_variable, reward_variable = Variable(state0_tensor.cuda()), Variable(state1_tensor.cuda()), Variable(action_tensor.cuda()), Variable(terminal1_tensor.cuda()), Variable(reward_tensor.cuda())
        else:
            state0_variable, state1_variable, action_variable, terminal1_variable, reward_variable = Variable(state0_tensor), Variable(state1_tensor), Variable(action_tensor), Variable(terminal1_tensor), Variable(reward_tensor)

        # Compute current Q value, q_func takes only state and output value for every state-action pair
        # We choose Q based on action taken.
        current_Q_values = self.navigation.model(state0_variable).gather(1, action_variable.unsqueeze(1)).squeeze(1)
        # Compute next Q value based on which action gives max Q values
        # Detach variable from the current graph since we don't want gradients for next Q to propagated
        next_max_Q = self.navigation.target_model(state1_variable).detach().max(1)[0]
        next_Q_values = terminal1_variable * next_max_Q
        # Compute the target of the current Q values
        target_Q_values = reward_variable + (constants.DQN_GAMMA * next_Q_values)
        # Compute Bellman error
        bellman_error = target_Q_values - current_Q_values
        # clip the bellman error between [-1 , 1]
        clipped_bellman_error = bellman_error.clamp(-1, 1)
        # Note: clipped_bellman_delta * -1 will be right gradient
        d_error = clipped_bellman_error * -1.0
        # Clear previous gradients before backward pass
        self.optimizer.zero_grad()
        # run backward pass
        current_Q_values.backward(d_error.data)

        # TODO: try this too
        # loss = F.smooth_l1_loss(current_Q_values, target_Q_values.unsqueeze(1))
        # loss.backward()

        # Perfom the update
        self.optimizer.step()
        self.num_param_updates += 1

        # Periodically update the target network by Q network to target Q network
        if self.num_param_updates % constants.DQN_TARGET_UPDATE_FREQ == 0:
            self.navigation.target_model.load_state_dict(self.navigation.model.state_dict())

        print ("updating policy: ", self.num_param_updates)

    def run(self):
        episode_steps = 0
        observation = None                                                                                
        while self.step < self.train_iter:
            self.sptm.clear()

            height = random.uniform(constants.DATA_COLLECTION_MIN_HEIGHT, constants.DATA_COLLECTION_MAX_HEIGHT)
            init_position = [random.uniform(-150.0, 150.0), random.uniform(-150.0, 150.0), -height]
            init_orientation = [0.0, 0.0, random.uniform(-math.pi, math.pi)]

            teach_position = init_position.copy()
            teach_orientation = init_orientation.copy()
            print (teach_position)

            # repeat_position, repeat_orientation = [10, 0, -6], [0, 0, 0]
            self.env.set_initial_pose(teach_position, teach_orientation)
            self.env.set_mode(constants.AIRSIM_MODE_TEACH)
            time.sleep(1)
            print ("Running teaching phase")
            self.teach()

            repeat_position = init_position.copy()
            repeat_orientation = init_orientation.copy()
            print (repeat_position)
            # repeat_position, repeat_orientation = [10, 4, -6], [0, 0, 0]
            repeat_position[0] = repeat_position[0] + random.uniform(-2., 2.)
            repeat_position[1] = repeat_position[1] + random.uniform(-2., 2.)
            repeat_position[2] = repeat_position[2] + random.uniform(-1., 1.)
            repeat_orientation[2] = repeat_orientation[2] + random.uniform(-math.pi / 8, math.pi / 8)
            self.env.set_initial_pose(repeat_position, repeat_orientation)
            self.env.set_mode(constants.AIRSIM_MODE_REPEAT)
            time.sleep(1)
            print ("Running repeating phase")
            self.repeat()

            if (self.step > constants.DQN_LEARNING_OFFSET_START and
                self.step % constants.DQN_LEARNING_FREQ == 0):
                self.update_policy()

            if (self.step % constants.DQN_CHECKPOINT_FREQ == 0):
                self.navigation.save_model(self.checkpoint_path, self.step) 

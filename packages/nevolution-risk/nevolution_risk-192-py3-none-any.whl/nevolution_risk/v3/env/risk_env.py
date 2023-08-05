import networkx as nx
import pygame

import gym
import numpy as np
from gym import spaces
from numpy import int32, float32

from nevolution_risk.constants.constants import DEFAULT_POS_PLAYER_2, DEFAULT_POS_PLAYER_1
from nevolution_risk.v3.logic import Graph
from nevolution_risk.v3.view import Gui


class RiskEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 10
    }

    node_count = 42
    player_count = 2
    troop_count = 5
    agent_troops_count = 0

    observation_space = spaces.Box(low=0, high=1, shape=[node_count * (player_count + troop_count + 2), ], dtype=int32)

    def __init__(self):
        self.player_positions = (DEFAULT_POS_PLAYER_1, DEFAULT_POS_PLAYER_2)
        self.graph = Graph(self.player_positions, self.player_count)
        self.static_agent = self.random_step
        self.gui = Gui(self.graph)
        self.current_player = 1
        self.done = False
        self.rendering = True
        self.first_render = True
        self.legal_actions = []
        for n in range(0, len(self.graph.nodes)):
            for adjacent in self.graph.nodes[n].adj_list:
                self.legal_actions.append((self.graph.nodes[n].id, adjacent.id, 1))
                self.legal_actions.append((self.graph.nodes[n].id, adjacent.id, 2))
        self.legal_actions.append((0, 0, 0))

        edges = []
        for line in nx.generate_edgelist(self.graph.graph):
            edges.append(line)
        edge_count = len(edges)
        self.action_space = spaces.Box(low=0, high=1, shape=[edge_count * 4 + 1, ], dtype=float32)
        self.action_len = len(self.action_space.sample())

    def set_static_agent(self, step_function):
        self.static_agent = step_function

    def set_start_positions(self, player_1, player_2):
        '''
        sets the starting position of the 2 player on the map
        also replaces the current graph with a new one

        :param player_1: position as one integer
        :param player_2: position as one integer
        :return:
        '''
        if player_1 == player_2:
            raise EnvironmentError('Players cannot start at the same node!')
        if player_1 > len(self.graph.nodes) - 1 or player_2 > len(self.graph.nodes) - 1:
            raise EnvironmentError('ID out of range.')
        self.player_positions = (player_1, player_2)
        self.graph = Graph(self.player_positions, self.player_count)

    '''
    action format:
        [probabilities]
    '''

    def step(self, action):
        '''
            simulates one step of the game that is being played
            the enemy turn is part of one step

            :param action: a list of values, shape is defined in he action_space
            :return: 4 results of the current step
                observation - game state after the step, shape defined in observation_space
                reward      - reward for the step
                done        - a boolean, which is true, when the match is over
                info        - a string which can display some information
        '''
        if self.done:
            self.reset()

        for i, valid_action in enumerate(self.graph.players[0].valid_actions):
            action[i] *= valid_action

        source_id = self.legal_actions[np.argmax(action)][0]
        target_id = self.legal_actions[np.argmax(action)][1]
        troops = self.legal_actions[np.argmax(action)][2]
        exit = False
        if troops == 0:
            exit = True

        if not exit:
            self.graph.move(source_id, target_id, troops, self.graph.players[0])
        elif exit:
            self.graph.next_player()
            exit = False
            while not exit:

                """
                ----------------------------------------------------------------------------------
                code for opponent AI goes here
                """
                observation = self._graph_to_one_hot(reverse=True)

                player2_action = self.static_agent(observation)

                for i, valid_action in enumerate(self.graph.players[1].valid_actions):
                    player2_action[i] *= valid_action

                source_id = self.legal_actions[np.argmax(player2_action)][0]
                target_id = self.legal_actions[np.argmax(player2_action)][1]
                troops = self.legal_actions[np.argmax(player2_action)][2]

                if troops == 0:
                    exit = True

                self.graph.move(source_id, target_id, troops, self.graph.players[1])
                """
                ----------------------------------------------------------------------------------
                """
            self.graph.next_player()

        observation = self._graph_to_one_hot()
        self.done = self.graph.is_conquered()

        reward = self.get_reward(self.graph.players[1])

        return observation, reward, self.done, {}

    def random_step(self, observation):
        return self.action_space.sample()

    def reset(self):
        '''
        replaces the current game state with a fresh one

        :return: observation of the new game state
        '''
        self.graph = Graph(self.player_positions, self.player_count)
        self.gui.graph = self.graph
        self.done = False
        self.rendering = True
        self.agent_troops_count = 0
        return self._graph_to_one_hot()

    def render(self, mode='human', control="auto"):
        '''
        draws the current games state into the pygame window and sleeps for 1/60 seconds

        :param mode:
        :param control: decides whether additional gui elements are displayed for human/machine control
        :return:
        '''
        if self.first_render:
            pygame.init()
            self.first_render = False

        if control == "auto":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
        if mode == 'rgb_array':
            return self.gui.render(mode)
        else:
            self.gui.render(mode)

        if control == "auto":
            pygame.display.update()

    def is_action_valid(self, action, player):
        '''
        checks if the player own the starting node

        :param action: a tuple containing start and end node on the graph
        :param player: object in the graph, which represents one player
        :return: true if the player owns the starting node
        '''
        if action[2] == 0:
            return True
        if self.graph.nodes[action[0]].player != player:
            return False
        if self.graph.nodes[action[0]].troops < action[2] + 1:
            return False
        if self.graph.nodes[action[1]].player == player:
            if self.graph.nodes[action[1]].troops + action[2] > 5:
                return False
        return True

    def update_valid_actions(self):
        '''
        iterates over the valid_actions array if all players and updates its values

        an action is valid, when the graph connects start and end node
        an action is legal, when none of the game rules are broken

        :return:
        '''
        for player in self.graph.players:
            valid_actions = np.zeros(self.action_len, dtype=float32)
            n = 0
            for action in self.legal_actions:
                if self.is_action_valid(action, player):
                    valid_actions[n] = 1
                n = n + 1
            player.valid_actions = valid_actions

    def _graph_to_one_hot(self, reverse=False):
        '''
        encodes the current game state via one hot encoding
        an integer encoded to one hot results in a array that is filled with zeros and only contains a 1 at the index
        of the integer

        example:
        space = 0-4
        integer = 3

        encode: [0,0,0,1,0]

        :param reverse: boolean, that if true, flips the players before encoding
        :return: an array that contains 0s and 1s to represent the current game state
        '''
        one_hot = np.zeros(0, int32)
        zero_array = np.zeros(5, int32)

        np.append(one_hot, zero_array)

        player1 = self.graph.players[0]
        player2 = self.graph.players[1]

        for n in range(0, len(self.graph.nodes)):
            if self.graph.nodes[n].player == player1:
                one_hot = np.append(one_hot, to_one_hot(1, self.player_count))
                one_hot = np.append(one_hot, to_one_hot(self.graph.nodes[n].troops, self.troop_count))
            elif self.graph.nodes[n].player == player2:
                one_hot = np.append(one_hot, to_one_hot(2, self.player_count))
                one_hot = np.append(one_hot, to_one_hot(self.graph.nodes[n].troops, self.troop_count))
            else:
                one_hot = np.append(one_hot, to_one_hot(0, self.player_count))
                one_hot = np.append(one_hot, to_one_hot(self.graph.nodes[n].troops, self.troop_count))

        self.update_valid_actions()

        return one_hot

    def get_reward(self, player):
        '''
        calculates the reward

        :param player: player object in the graph
        :return: the current reward
        '''
        total_troops = 0

        for n in range(0, len(self.graph.nodes)):
            if self.graph.nodes[n].player == player:
                total_troops += self.graph.nodes[n].troops

        reward = total_troops - self.agent_troops_count
        self.agent_troops_count = total_troops
        return reward


def to_one_hot(n, limit):
    if n < 0:
        raise IndexError("number must not be negative")
    array = np.zeros(limit + 1, np.int32)
    array[n] = 1
    return array


if __name__ == '__main__':
    print(np.zeros(0, int32))

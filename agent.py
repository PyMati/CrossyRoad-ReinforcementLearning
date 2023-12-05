from platform import node
from player import Player
from gameboard import Gameboard
import random
import numpy as np


class Node:
    def __init__(self, action, state, reward):
        self.action = action
        self.state = state
        self.reward = reward
        self.visits = 1
        self.children = []
        self.parent = None

    def __str__(self) -> str:
        return f"""
            {self.action,
            self.state,
            self.reward,
            self.visits,
            self.children,
            self.parent,}
            """


class MonteCarloAgent:
    def __init__(self, agent_player: Player, gameboard: Gameboard):
        self.agent = agent_player
        self.gameboard = gameboard

        self.exploration_factor = 1.41
        self.counter = 0

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent

    def simulate(self, action):
        agent_pos = self.agent.get_player_pos()
        new_state = agent_pos

        if action == self.agent.go_left:
            new_state = [agent_pos[0], agent_pos[1] - 1]
        elif action == self.agent.go_right:
            new_state = [agent_pos[0], agent_pos[1] + 1]
        elif action == self.agent.go_down:
            new_state = [agent_pos[0] + 1, agent_pos[1]]

        return new_state

    def expand_tree(self, node: Node):
        possible_actions = self.agent.get_possible_actions()
        child_nodes = []

        for action in possible_actions:
            new_state = self.simulate(action)
            reward = self.gameboard.get_reward(new_state)
            child_node = Node(action, new_state, reward)
            child_node.parent = node
            node.children.append(child_node)
            child_nodes.append(child_node)

        return child_nodes

    def select_best_child(self, node: Node):
        best_child = max(
            node.children,
            key=lambda child: (child.reward / child.visits)
            + self.exploration_factor
            * np.sqrt(np.log(node.visits) / (child.visits + 1)),
        )
        return best_child

    def select_node(self, node: Node):
        while node.children:
            node = self.select_best_child(node)

        return node

    def play_game(self):
        if self.counter > 10 and self.agent.is_dead == False:
            self.counter = 0
            root = Node(None, self.gameboard.get_env_state(), 0)

            for _ in range(100):
                selected_node = self.select_node(root)
                child_nodes = self.expand_tree(selected_node)
                best_child = self.select_best_child(selected_node)
                action = best_child.action
                state = self.simulate(action)
                reward = self.gameboard.get_reward(state)
                self.backpropagate(best_child, reward)

            print(self.gameboard.reward_map)
            best_action = max(root.children, key=lambda child: child.visits).action
            self.agent.take_action(best_action)

        self.counter += 1

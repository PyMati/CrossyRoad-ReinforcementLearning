from copy import deepcopy
from player import Player
from gameboard import Gameboard
import random
import numpy as np


class Node:
    def __init__(self, action, state: Gameboard, player_state: Player, reward):
        self.action = action
        self.state = state
        self.reward = reward
        self.player_state = player_state
        self.visits = 0
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
    def __init__(self, agent_player, gameboard):
        self.agent = agent_player
        self.gameboard = gameboard
        self.exploration_factor = 1.41
        self.counter = 0

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent

    def simulate(self, node: Node):
        env, player = self.make_state_copy(node.state, node.player_state)
        reward = 0

        if player.has_won:
            return 1
        if player.is_dead:
            return 0

        while not player.is_dead and not player.has_won:
            env.develop_game()
            actions = player.get_possible_actions()
            # print(player.is_dead, player.has_won)
            if player.has_won:
                reward = 1
                break
            if player.is_dead:
                reward = 0
                break
            reward += env.get_reward(player.get_player_pos())
            action = random.choice(actions)
            # print(player.get_player_pos(), action, env.reward_map)
            if action.__name__ == "go_down":
                player.go_down()
            elif action.__name__ == "go_left":
                player.go_left()
            elif action.__name__ == "go_right":
                player.go_right()
            else:
                player.go_up()

        return reward

    def expand_tree(self, node: Node):
        possible_actions = node.player_state.get_possible_actions()

        for action in possible_actions:
            env, player = self.make_state_copy(node.state, node.player_state)
            env.develop_game()

            if action.__name__ == "go_down":
                player.go_down()
            elif action.__name__ == "go_left":
                player.go_left()
            elif action.__name__ == "go_right":
                player.go_right()
            else:
                player.go_up()

            child_node = Node(action, env, player, 0)
            child_node.parent = node
            node.children.append(child_node)

        return node.children

    def select_best_child(self, node):
        if not node.children:
            return node

        best_child = max(
            node.children,
            key=lambda child: (child.reward / child.visits)
            + self.exploration_factor
            * np.sqrt(
                np.log(node.visits) / child.visits if child.visits > 0 else float("inf")
            )
            if child.visits > 0
            else float("inf"),
        )

        return best_child

    def select_node(self, node):
        return self.select_best_child(node)

    def make_state_copy(self, env: Gameboard, player: Player):
        new_env = deepcopy(env)
        new_player = deepcopy(player)
        new_env.players = [new_player]
        return new_env, new_player

    def play_game(self):
        if self.counter > 9 and not self.agent.is_dead:
            self.counter = 0

            env, player = self.make_state_copy(self.gameboard, self.agent)

            root = Node(None, env, player, 0)

            for _ in range(1000):
                node = root
                while len(node.children) != 0:
                    node = self.select_node(node)

                self.expand_tree(node)
                node = self.select_node(node)
                score = self.simulate(node)
                self.backpropagate(node, score)

            print("-" * 100)
            for child in root.children:
                print(child.visits, child.reward, child.action)
            best_child = max(root.children, key=lambda child: child.visits)
            print("-" * 100)
            print(best_child)
            best_action = best_child.action

            if best_action.__name__ == "go_down":
                self.agent.go_down()
            elif best_action.__name__ == "go_left":
                self.agent.go_left()
            elif best_action.__name__ == "go_right":
                self.agent.go_right()
            else:
                self.agent.go_up()

        self.counter += 1

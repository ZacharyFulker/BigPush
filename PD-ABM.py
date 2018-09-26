import random
from itertools import accumulate
import numpy as np


# create class for agents
class Player:
    def __init__(self, cooperate, defect, num_players):
        self.cooperate = cooperate
        self.defect = defect
        self.win_total = 0
        self.adj_matrix = np.ones((1, num_players), dtype=float)
        self.adj_matrix[0][0] = 0

    def choose_strategy(self):
        defect_ratio = self.defect / (self.cooperate + self.defect)
        if random.uniform(0, 1) <= defect_ratio:
            defect = True
        else:
            defect = False
        return defect

    def update(self, defect, round_winnings, index):
        if defect:
            self.defect += round_winnings
        else:
            self.cooperate += round_winnings
        self.win_total += round_winnings
        self.adj_matrix[0][index] += round_winnings

    def get_adj_matrix(self):
        return self.adj_matrix


def run_game_network(payoffs, rounds, num_players):
    # initialize agents
    agents = []
    for player in range(num_players):
        agents.append(Player(1, 1, num_players))
    # begin game
    for iteration in range(rounds):
        # each agent chooses an opponent in each round
        for index in range(len(agents)):
            adj_matrix = agents[index].get_adj_matrix()
            random_num = random.uniform(0, sum(adj_matrix)[0])
            for opponent_index, item in enumerate(accumulate(adj_matrix)[0]):
                if random_num <= item:
                    break
            # agents pick strategy and then update based on game results
            opponent_defect = agents[opponent_index].choose_strategy()
            agent_defect = agents[index].choose_strategy()
            agent_winnings = payoffs[agent_defect][opponent_defect]
            opponent_winnings = payoffs[opponent_defect][agent_defect]
            agents[index].update(agent_defect, agent_winnings, opponent_index)
            agents[opponent_index].update(opponent_defect, opponent_winnings, index)
    return agents


# Game Setup and execution
payoff = [[1, 0], [(2/3), (1/3)]]
results = run_game_network(payoff, 5, 10)
#for i in list(range(len(agents))):
    #print('Player: ', i)
    #print(results[i].win_total)
    #print(results[i].defect)
    #print(results[i].cooperate)

#try to get sense of how system is evolving, Change payoffs see what happens
#statistic that shows proportion of how likely  to cooperate over time and plot it


# Junk
# each agent selects randomly (with equal likelyhood) one other agent to play for their turn in the round), total games in each round is number of agents
def run_game(agents, payoffs, rounds):
    for round in list(range(rounds)):
        for agent in agents:
            other_agents = list(agents)
            other_agents.remove(agent)
            opponent = other_agents[random.randint(0, len(other_agents) - 1)]
            opponent_defect = opponent.choose_strategy()
            agent_defect = agent.choose_strategy()
            agent_winnings = payoffs[agent_defect][opponent_defect]
            opponent_winnings = payoffs[opponent_defect][agent_defect]
            agent.update(agent_defect, agent_winnings)
            opponent.update(opponent_defect, opponent_winnings)
    return agents
#adj_matrix = [[0,.5,0,.5,0,0], [.5,0,.5,0,0,0], [0,.5,0,0,0,.5], [.5,0,0,0,.5,0], [0,0,0,.5,0,.5], [0,0,.5,0,.5,0]] #look for multinomial choice option
#p1 = Player(1, 1, 10)
#p2 = Player(1, 1)
#p3 = Player(1, 1)
#p4 = Player(1, 1)
#p5 = Player(1, 1)
#p6 = Player(1, 1)
#agents = [p1, p2, p3, p4, p5, p6]
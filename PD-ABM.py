import random


# create class for agents
class Player:
    def __init__(self, cooperate, defect):
        self.cooperate = cooperate
        self.defect = defect
        self.win_total = 0

    def update(self, opponent_defect, round_winnings):
        if opponent_defect:
            self.defect = self.defect + 1
        else:
            self.cooperate = self.cooperate + 1
        self.win_total = self.win_total + round_winnings

    def choose_strategy(self):
        defect_ratio = self.defect / (self.cooperate + self.defect)
        if random.uniform(0, 1) <= defect_ratio:
            defect = True
        else:
            defect = False
        return defect


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
            agent.update(opponent_defect, agent_winnings)
            opponent.update(agent_defect, opponent_winnings)
    return agents

#
def run_game_network(agents, payoffs, rounds, adj_matrix):
    for round in list(range(rounds)):
        for i in range(len(agents)): ####
            prob_sum = 0
            for opponent_index, item in enumerate(adj_matrix[i]):
                prob_sum = item + prob_sum
                if random.random(0, 1) <= prob_sum:
                    break
            opponent_defect = agents[opponent_index].choose_strategy()
            agent_defect = agents[i].choose_strategy()
            agent_winnings = payoffs[agent_defect][opponent_defect]
            opponent_winnings = payoffs[opponent_defect][agent_defect]
            agents[i].update(opponent_defect, agent_winnings)
            agents[opponent_index].update(agent_defect, opponent_winnings)
    return agents

# Game Setup and execution
payoffs = [[3, 0], [2, 1]]
adj_matrix = [[0,.5,0,.5,0,0], [.5,0,.5,0,0,0], [0,.5,0,0,0,.5], [.5,0,0,0,.5,0], [0,0,0,.5,0,.5], [0,0,.5,0,.5,0]] #look for multinomial choice option
p1 = Player(1, 1)
p2 = Player(1, 1)
p3 = Player(1, 1)
p4 = Player(1, 1)
p5 = Player(1, 1)
p6 = Player(1, 1)
agents = [p1, p2, p3, p4, p5, p6]
results = run_game_network(agents, payoffs, 5, adj_matrix)
for i in list(range(len(agents))):
    print('Player: ', i)
    print(results[i].win_total)
    print(results[i].defect)
    print(results[i].cooperate)

#switch to payoff reinforcement
#reinforce link weights in same way (so strategy and links coevolve)
#Start with complete networks that evolves based on payoffs (np.ones - np.diagonal zeros)
#try to get sense of how system is evolving, Change payoffs see what happens
#statistic that shows proportion of how likely  to cooperate over time and plot it
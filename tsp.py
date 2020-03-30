import random
from math import hypot
from itertools import permutations
import networkx as nx
import mlrose


class State:
    nodes = 8
    width = 100

    # Generate random graph
    # Note: the class variable G will be generated once and shared between instances
    G = nx.Graph()

    x_coords = random.sample(range(1, width), nodes)
    y_coords = random.sample(range(1, width), nodes)
    coords = [(x, y) for x, y in zip(x_coords, y_coords)]

    for i in range(nodes):

        G.add_node(i, coord=coords[i])

        for j in range(i):
            x_i, y_i = G.nodes[i]['coord']
            x_j, y_j = G.nodes[j]['coord']
            G.add_edge(i, j, weight=hypot(x_i - x_j, y_i - y_j))

    true_tsp_value = 0  # TODO modify this


    def __init__(self, visited=None):

        # visited will have the nodes in order they were traversed
        if (not visited):
            self.visited = list()
        else:
            self.visited = visited


    #
    def get_genetic_path(self):
        """
        Return an approximate solution length to the TSP problem
        """

        fitness_coords = mlrose.TravellingSales(coords=self.coords)

        dist_list = list(self.G.edges.data('weight'))
        fitness_dists = mlrose.TravellingSales(distances=dist_list)

        problem_fit = mlrose.TSPOpt(length=self.nodes, fitness_fn=fitness_coords, maximize=False)

        best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2, mutation_prob=0.2,
                                                      max_attempts=100)

        return best_fitness


    def get_optimal_path(self):
        """
        Return the optimal TSP solution length
        """

        min_length = 100000000000

        for path in permutations(self.G.nodes()):
            length = self.get_path_length(path=path)
            if (length < min_length):
                min_length = length

        return min_length


    def get_path_length(self, path=None):
        """
        Get the length of the specified path. If none is specified, return the length of 'visited' list
        """
        if not path:
            path = self.visited

        length = 0

        for node in range(self.nodes - 1):
            length += self.G[path[node]][path[node + 1]]['weight']

        length += self.G[path[0]][path[self.nodes - 1]]['weight']

        return length


def GetActions(CurrentState):
    """
    Get set of nodes not yet visited
    """

    available_nodes = set(CurrentState.G.nodes).difference(set(CurrentState.visited))
    return available_nodes


def ApplyAction(CurrentState, Action):
    """
    Get the next state that results from visiting node 'Action'
    """
    new_visited = list(CurrentState.visited).append(Action)
    new_state = State(new_visited)
    return new_state


def GetNextStates(CurrentState):
    # get unexplored nodes
    unexplored_nodes = GetActions(CurrentState)
    if not unexplored_nodes:
        return None

    next_states = []
    for node in unexplored_nodes:
        new_state = ApplyAction(CurrentState, node)
        next_states.append(new_state)
    return next_states


def IsTerminal(CurrentState):

    if (len(CurrentState.visited) == CurrentState.nodes):
        return True


def GetStateRepresentation(CurrentState):

    return (CurrentState.visited[-1], CurrentState.visited)


def GetResult(CurrentState):

    if (IsTerminal(CurrentState)):
        if (CurrentState.get_path_length() <= CurrentState.true_tsp_value * 1.1):
            return 1

    return 0


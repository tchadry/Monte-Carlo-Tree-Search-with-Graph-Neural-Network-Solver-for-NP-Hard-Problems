import random
from math import hypot
from itertools import permutations
import networkx as nx
import mlrose


class State:
    nodes = 6
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


    # Compute optimal path length

    optimal_value = 100000000000

    for path in permutations(G.nodes()):
        #length = self.get_path_length(path=path)

        length = 0

        for node in range(nodes - 1):
            length += G[path[node]][path[node + 1]]['weight']

        length += G[path[0]][path[nodes - 1]]['weight']

        if (length < optimal_value):
            optimal_value = length


    def __init__(self, visited=None):

        # visited will have the nodes in order they were traversed



        if (not visited):
            self.visited = list()
            self.last_visited = None
        else:
            self.visited = visited
            self.last_visited = visited[-1]


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

        return self.optimal_value




    def get_path_length(self, path=None):
        """
        Get the length of the specified path. If none is specified, return the length of 'visited' list
        """
        if not path:
            path = self.visited

        length = 0

        #TODO delete
        if (len(path) != self.nodes):
            print(f'\nWARNING: The path passed to "get_path_length()" is {len(path)}. (#nodes = {self.nodes})\n')

        for node in range(len(path) - 1):
            length += self.G[path[node]][path[node + 1]]['weight']

        length += self.G[path[0]][path[len(path) - 1]]['weight']

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
    new_visited = list(CurrentState.visited)
    new_visited.append(Action)
    new_state = State(new_visited)
    return new_state


def GetNextStates(CurrentState):
    # get unexplored nodes
    unexplored_nodes = GetActions(CurrentState)
    if not unexplored_nodes:
        return []

    next_states = []
    for node in unexplored_nodes:
        new_state = ApplyAction(CurrentState, node)
        next_states.append(new_state)
    return next_states


def IsTerminal(CurrentState):
    if (len(CurrentState.visited) == CurrentState.nodes):
        #print('SSSSSSSSSS')
        return True

    return False


def GetStateRepresentation(CurrentState):

    return (CurrentState.last_visited, CurrentState.visited)


def GetResult(CurrentState):

    if (IsTerminal(CurrentState)):
        if (CurrentState.get_path_length() <= CurrentState.optimal_value * 1.1):
            return 1
        else:
            return 0
    else:
        print(f'\nWARNING: GetResult was passed a non-terminal state. Only terminal states have the result property.'
              f'\nThe state that was passed: {CurrentState.visited}\n')
        return 0


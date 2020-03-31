import node as nd
import numpy as np
import MCTS as mcts
import tsp as game
import random

'''

The starting node will be randomized since for a hamiltonian cycle, independent of the node you start, if there is a solution
you should be able to find one.

For this problem, we will only test inputs which we know there a Hamiltonian cycle exist
'''


n = game.State.nodes

first_node = random.randint(0,n-1)

visited = [first_node]

print(f'First node: {first_node}')

#initializing tree
RootState = game.State(visited)
#print(RootState.visited)
#input()

Root = nd.Node(RootState)
#print(Root.state.visited)
#input()
print("Nodes created")

x = mcts.MCTS(Root,game)
print("MCTS created")

x.Run()

print("Iterations finished")

#we are going to start from the root node in the resulting MCTS tree, and do a DFS to pick the maximum value node at each level, until we
#get to a leaf node (terminal state). The resulting path will be the optimal result from the MCTS
result=[]
child=False

#print(Root.state.visited)
#input()

if len(Root.children)>0:
    child=True
while (child):
    max=-1
    children = Root.children
    #print(children)
    #print(Root)
    #input()

    for i in children:
        if i.sputc>max:
            max=i.sputc
            Root = i

    #if (len(children) == 1):
    #    print(children[0].sputc)
    #    input()

    #result.append(game.GetStateRepresentation(Root.state)[0])
    #print(Root.state.visited)
    #print(result)
    #input()
    if (len(Root.children)==0):
        child=False

print(Root.state.visited)

print(f'Optimal value: {Root.state.optimal_value}')
print(f'Solution value: {Root.state.get_path_length()}')
print(f'Random value: {Root.state.get_path_length(list(range(n)))}')

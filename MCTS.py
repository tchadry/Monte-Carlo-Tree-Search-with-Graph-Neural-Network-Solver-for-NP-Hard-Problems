import node as nd
import numpy as np
import random
'''
Game agnostic MCTS
Inspired by github : https://github.com/sergeim19/SinglePlayerMCTS
In this file, we implemented the MCTS process that solves a single player
game without having any domain knowledge. The main methods we had to implement were
the selection, expansion, simulation and backpropagation, using helper methods to do so.
The evaluation method we chose to evaluate the nodes was the Upper Confidence Bound (UCT).
The actual final result of the terminal state nodes comes from the game implementation 
'''


class MCTS:

    #will be initiated on the root node
    #for now use verbose = true to print steps during search
    def __init__(self, Node,game):
        self.root = Node
        self.verbose = True
        self.game=game

    #implement selection step
    def selection(self):
        currentNode = self.root
        #assume no children but check for it
        children = False
		# Check if child nodes exist.
        if(len(currentNode.children) > 0):
	        children = True

        #now, we will look through all children and select their children
        #while there are still children left
        while(children):
            #next node selected will be based on weights
            currentNode = self.selectNode(currentNode)

            #we check if now the current node has any children
            if(len(currentNode.children)==0):

                children=False
            currentNode.visits += 1

        #return the node - will be a leaf node
        return currentNode

    def selectNode(self, Node):
        #given a node, select the next node from its children based on the number
        #of visits or the weights
        #we will choose first based on the number of visits
        #then on the evaluation method

        #if no children
        nextNode=Node


        for child in Node.children:
            if child.visits ==0:
                return child

        #if all childs have been visited, we will use the weights assigned
        #during evaluation method
        max=0
        for child in Node.children:
            weight = child.sputc
            if weight >max:
                max=weight
                nextNode = child
        return nextNode

    #check if current node is a leaf/terminal node
    def is_final_state(self, Node):
        if (self.game.IsTerminal(Node.state)):
            return True
        return False


    #find out if node has a parent
    def has_parent(self,Node):
        if (Node.parent):
            return True
        return False

    #find the level of the node by looking at its parents
    def Node_level(self,Node):
        level = 0

        #iterate through the parents until root node 
        while(Node.parent):
            level+=1
            Node = Node.parent

        return level




    #now we can do expansion of MCTS, starting from a leaf node
    def expansion(self, Node):

        #check if the leaf node is a final state in the game
        if(self.is_final_state(Node)):
            return False

        elif(Node.visits==0):
            return Node

        #if these cases are not true, then we expand by creating
        #the new states from the current state. We know it is # NOTE:
        #a final state
        if(len(Node.children)==0):
            #get the new children nodes
            children = self.eval_next_states(Node)
            for child in children:
                if(np.all(child.state==Node.state)):
                    continue
                else:
                    Node.add_child(child)

        #now we are going to select the next child randomly
        assert(len(Node.children)>0), "no children"
        i = np.random.randint(0, len(Node.children))
        return Node.children[i]




    def eval_next_states(self,Node):
        #will evaluate the possible children states of the current node and return then
        #GAME NEEDS TO BE ABLE TO CREATE NEW STATES GIVEN CURRENT STATES
        next_states = self.game.GetNextStates(Node.state)

        children = []
        for state in next_states:
             #create new node
            new_node = nd.Node(state)

             #add node to children
            children.append(new_node)

        #return the list of Children
        return children

    #now we can perform the simulation step of the MCTS
    def Simulation(self,Node):

        print("Simulation on")

        #get current state and node
        currentState=Node.state
        currentLevel=self.Node_level(Node)

        end=self.game.IsTerminal(currentState)

        while(end==False):
            state = self.game.GetNextStates(currentState)
            currentLevel+=1

            end = self.game.IsTerminal(state)

        return self.game.GetResult(currentState)

    def Backprop(self,Node,result):
        current = Node
        current.wins+= result
        current.visits +=1

        #add to the result square
        current.ressq += result**2

        self.node_evaluation(current)

        #now we back propagate through the parents, updating their values also 
        while(self.has_parent(current)):
            current = current.parent
            current.wins+= result
            current.visits +=1
            current.ressq += result**2
            self.node_evaluation(current)

    def node_evaluation(self,Node):
        #now we can evaluate the node based on the number of visits, wins and
        # sum squared of the results

        if (Node.parent!=None):
            parent_visit = Node.parent.visits
        else:
            parent_visit = Node.visits
        UTC = (Node.wins/Node.visits) + 0.5*np.sqrt(np.log(parent_visit)/Node.visits)

        Mod = np.sqrt((Node.ressq-Node.visits*(Node.wins/Node.visits)**2+10000)/Node.visits)

        Node.sputc = UTC+Mod
        return Node.sputc

    #tested different values for iteration, 8000 gave us a fast running time and consistent results 
    def Run(self, MAXITER = 8000):
        #run over max iteration
        for i in range(MAXITER):

            #do selection, expansion, simulation and backpropagation 
            first = self.selection()
            second = self.expansion(first)

            #do simulation and backpropagation on the second node only if the first was
            #not a terminal state
            if(second==True ):
                result = self.Simulation(second)
                self.Backprop(second,result)

            else:
                result = self.game.GetResult(first.state)

                self.Backprop(first,result)

        

      
        

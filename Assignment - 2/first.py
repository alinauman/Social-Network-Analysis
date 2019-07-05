import snap
import random
import matplotlib.pyplot as plt
import numpy

def first_part():
    #Loading the sample data of Epinions
    Graph = snap.LoadEdgeList(snap.PNGraph,"soc-Epinions1.txt",0,1)
    #Getting the Strongly and Weakly Connected part of the graph
    SCC = snap.GetMxScc(Graph)
    WCC = snap.GetMxWcc(Graph)
    #Loading all the Strongly Connected Nodes 
    SCC_nodes = []
    for strong_nodes in SCC.Nodes():
        SCC_nodes.append(strong_nodes.GetId())
    print("Strongly Connected Nodes: ", len(SCC_nodes))
    
    #Running the BFS on one of the nodes of SCC to find out nodes         
    BFS_Out_Nodes = snap.GetBfsTree(Graph, SCC_nodes[0], True, False)
    print("Initial Out Nodes: ",BFS_Out_Nodes.GetNodes())
    
    BFS_Out_Nodes_List = []
    for nodes in BFS_Out_Nodes.Nodes():
        if (nodes.GetId() not in SCC_nodes):
            BFS_Out_Nodes_List.append(nodes.GetId())
    
    for nodes in BFS_Out_Nodes.Nodes():
        if (nodes.GetId() in SCC_nodes):
             BFS_Out_Nodes.DelNode(nodes.GetId())
                      
    print('Out Nodes after deleting SCC Nodes', BFS_Out_Nodes.GetNodes())
    
    #Running the BFS on one of the nodes of SCC to find in nodes   
    BFS_In_Nodes = snap.GetBfsTree(Graph, SCC_nodes[0], False, True)
    print("Initial In Nodes: ",BFS_In_Nodes.GetNodes())
    
    BFS_In_Nodes_List = []
    for nodes in BFS_In_Nodes.Nodes():
        if (nodes.GetId() not in SCC_nodes):
            BFS_In_Nodes_List.append(nodes.GetId())
    
    for nodes in BFS_In_Nodes.Nodes():
        if (nodes.GetId() in SCC_nodes):
             BFS_In_Nodes.DelNode(nodes.GetId())
    
    print('In Nodes after deleting SCC Nodes', BFS_In_Nodes.GetNodes())
    
    """Now we need to find the In Tendrils
        and Out Tendrils along with the nodes
        in Tubes and the Disconnected Nodes"""
    Out_Nodes = snap.GetBfsTree(BFS_In_Nodes, BFS_In_Nodes_List[0], True, False)
    In_Nodes = snap.GetBfsTree(BFS_Out_Nodes, BFS_Out_Nodes_List[0], False, True)
    
    In_Tendrils = []
    Out_Tendrils = []
    
    for node in Out_Nodes.Nodes():
        In_Tendrils.append(node.GetId())
    
    for node in In_Nodes.Nodes():
        Out_Tendrils.append(node.GetId())
        
    print("In Tendril - Nodes: ", len(In_Tendrils))
    print("Out Tendril - Nodes: ", len(Out_Tendrils))
    
    #Nodes in Tubes
    Tubes_Nodes = []
    for nodes in Out_Nodes.Nodes():
        if nodes in In_Nodes.Nodes():
            Tubes_Nodes.append(nodes.GetId())
            
    print("Nodes in Tube: ",len(Tubes_Nodes))
    
    #All the disconnected nodes which are not part of the SCC, IN, OUT, Tendrils and Tubes
    Disconnected_Nodes = []
    for nodes in Graph.Nodes():
        if (nodes.GetId() not in SCC_nodes) and (nodes.GetId() not in BFS_Out_Nodes_List) and (nodes.GetId() not in BFS_In_Nodes_List) and (nodes.GetId() not in In_Tendrils) and (nodes.GetId() not in Out_Tendrils):
            Disconnected_Nodes.append(nodes.GetId())
    
    print("All the Disconnected Nodes: ",len(Disconnected_Nodes))
	
def random_pair(x, r):
    #Loading the sample data of Epinions
    Graph = snap.LoadEdgeList(snap.PNGraph,"soc-Epinions1.txt",0,1) 
    # Extracting and appending Total number of nodes in the network
    nodes_total = []
    for node in Graph.Nodes():
        nodes_total.append(node.GetId())
    
    l = len(nodes_total)     
    rand_nodes = 10
    probability = []
    xmap = []
    for i in range(r):
        local_pairs = []
        for pairs in range(rand_nodes):
            pair_one = random.randint(0,l)
            pair_two = random.randint(1,l - 1)
            local_pairs.append((nodes_total[pair_one],nodes_total[pair_two]))
            
        xmap.append(rand_nodes)        
        Node_Pair_List = 0
        
        for item in local_pairs:
            a, b = item
            NIdToDistH = snap.TIntH()
            snap.GetShortPath(Graph, a, NIdToDistH, True)
            if b in NIdToDistH and NIdToDistH[b] > 0:
                Node_Pair_List = Node_Pair_List + 1
            
        #print(Node_Pair_List)
        #print(len(local_pairs))
        value = float(Node_Pair_List) / float(len(local_pairs))
        probability.append(value)
        #Doubling the Random Pair for plotting the graph the pairs and probabilities
        rand_nodes = rand_nodes * 2
    plt.plot(xmap, probability)
    plt.xlabel("No. of Nodes")    
    plt.ylabel("Probability")
    plt.show()
    #print(probability)
    return xmap, probability

list_probability = []       
def main():
    first_part()
    x = []
    n = int(raw_input("Please enter the number of node pairs:"))
    list_probability = random_pair(x, n)
    print(list_probability)
main()
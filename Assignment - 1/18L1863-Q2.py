import snap
import random

# Clustering Coeffiecent 
def clustering_coffecient(G):    
    cluster_dict = []    
    nodes = [] 
    # All nodes are stored   
    for s in G.Nodes():
        nodes.append(s.GetId())
    k = len(nodes)
        
    if (k > 2):
        for s in nodes:
            neighbors_node=[]
            neighbors_mutual=[]
            # node ids of all the nodes that are at distance Hop from node StartNId
            NodeVec = snap.TIntV()
            snap.GetNodesAtHop(G, s, 1, NodeVec, False)
            # nodes are stored for comparing
            for neighbor in NodeVec:
                neighbors_node.append(neighbor)
                
            for neighbor_2 in NodeVec:
                Second_NodeVec = snap.TIntV()
                snap.GetNodesAtHop(G, neighbor_2, 1, Second_NodeVec, False)
                # Finding triangles
                for second_neighbor in Second_NodeVec:
                    if second_neighbor in neighbors_node:
                       neighbors_mutual.append(second_neighbor)
                    
            
            neighbors_mutual = list(neighbors_mutual)
            
            clust_node = 0
            
            if len(neighbors_mutual):
                # Clustering Coefficient for each node
                clust_node =  (float(len(neighbors_mutual)))/((float(len(NodeVec)) * (float(len(NodeVec)) - 1)))
            
            cluster_dict.append(clust_node)
    else:
        pass
    
    # Average Clustering Coefficient for all nodes in a graph
    Average_Value = 0
    l = len(cluster_dict)
    if (l is not 0):
        for val in cluster_dict:
            Average_Value = Average_Value + val
            
        return Average_Value/ l
    else:
        return 0
    
# Erdos-Renyi Function
def Erdos_Renyi(G, p):
    for n1 in G.Nodes():
        for n2 in G.Nodes():
            # Removing Self-Loops
            if(n1.GetId() != n2.GetId()):
                # Comparison with the user generated probability
                r = random.random()
                if r <= p:
                    G.AddEdge(n1.GetId(), n2.GetId()) # Add edges using the probability - Undirected Graph
                else:
                    continue

# Small World Network
def first_edges(G):
    """
    begin with n nodes arranged as a ring, i.e., 
    imagine the nodes form a circle and each node 
    is connected to its two direct neighbors 
    (e.g., node 0 is connected to nodes 1 and n-1), giving us n edges
    """
    array = []
    
    for s in G.Nodes():
        array.append(s.GetId())
        
    count = len(array)
    first_index = 0
    second_index = 1
    last_index = -1
    
    for i, val in enumerate(array):
        first_index = i 
        if(second_index >= count):
            second_index = 0
        if(last_index >= count):
            last_index = 0
        first_id = array[first_index]
        second_id = array[second_index]
        last_id = array[last_index]
        
        if G.IsEdge(first_id, second_id) or (first_id == second_id):
            pass  
        else:
            G.AddEdge(first_id, second_id)
   
        if G.IsEdge(first_id, last_id) or (first_id == last_id):
            pass       
        else:
            G.AddEdge(first_id, last_id)

        second_index = second_index + 1
        last_index = last_index + 1 
           
def second_edges(G):
    """
    connect each node to the neighbors of its neighbors 
    (e.g., node 0 is also connected to nodes 2 and n-2). 
    This gives us another n edges.
    """
    array1 = []
    
    for s in G.Nodes():
        array1.append(s.GetId())
        
    count = len(array1)
    first_index = 0
    second_index = 2
    last_index = -2
    
    for i, val in enumerate(array1):
        first_index = i 
        if(second_index >= count):
            second_index = 0
        if(last_index >= count):
            last_index = 0
        first_id = array1[first_index]
        second_id = array1[second_index]
        last_id = array1[last_index]
        
        if G.IsEdge(first_id, second_id) or (first_id == second_id):
            pass            
        else:
            G.AddEdge(first_id, second_id)
   
        if G.IsEdge(first_id, last_id) or (first_id == last_id):
            pass       
        else:
            G.AddEdge(first_id, last_id)

        second_index = second_index + 1
        last_index = last_index + 1 
          
def random_edges(G, x):
    """
    Randomly select x pairs of nodes not yet connected 
    and add an edge between them.
    """
    array2 = []
    
    for s in G.Nodes():
        array2.append(s.GetId())
        
    """
    Create an empty array to include all nodes
    which have no edges between them to traverse.
    """
    array_NWNE = []
    '''
    To avoid multiple pairs in an array
    we will create a variable and iterate forward
    '''
    i = 0
    
    for j in array2:
        for index, k in enumerate(array2):
            if(index > i):
                if(G.IsEdge(j, k)):
                    pass 
                else:
                    if(j != k):
                        pair = (j, k)
                        array_NWNE.append(pair)
                        
    i = i + 1
    
    count = x
    while count > 0:
        r_num = random.randint(0, x)
        node_1, node_2 = array_NWNE[r_num]
        if(not G.IsEdge(node_1, node_2)):
            G.AddEdge(node_1, node_2)
            count = count - 1
                
# Empty Graph
def Empty_graph(n):
    G = snap.TUNGraph().New()
    for i in range(n):
        G.AddNode(i)
        
    return G
                        
def main():
    # Number of nodes
    n = int(raw_input("Please enter the number of nodes"))
    # Probability of an edge between nodes
    p = float(raw_input("Please enter the value of probability of an edge between nodes"))
    # Random Input of x pairs of nodes
    x = int(raw_input("Please enter the number of random, x pairs of nodes:"))
    # Empty graph and add nodes 
    ERM = Empty_graph(n)
    
    # Add edges to the graph using personal Erdos Renyi Model
    Erdos_Renyi(ERM, p)
    # Erdos Renyi Clustering Coeffecient
    print("Clustering Coeffecient: ", clustering_coffecient(ERM))
    # Diameter
    diameter_ERM = snap.GetBfsEffDiamAll(ERM, 10, False)
    print(diameter_ERM[2])
    # Largest Strongly Connected Component
    print("Largest Strongly Connected Component - Maximum size:", snap.GetMxSccSz(Small_world))
    # Largest Size of Graph
    ERM_size = snap.GetMxScc(ERM).GetEdges()
    print(ERM_size)
    # Plot of Degree Distribution
    snap.PlotOutDegDistr(ERM, "ERMGraph", "ERM Degree Distribution")
    
    # Add Small World Network
    Small_world = Empty_graph(n)
    first_edges(Small_world)
    second_edges(Small_world)
    random_edges(Small_world, x)
    # Small World Clustering Coeffecient
    print("Clustering Coeffecient: ", clustering_coffecient(Small_world))
    # Diameter
    diameter_Small_world = snap.GetBfsEffDiamAll(Small_world, 10, False)
    print(diameter_Small_world[2])
    # Largest Strongly Connected Component
    print("Largest Strongly Connected Component - Maximum size:", snap.GetMxSccSz(Small_world))
    # Largest Size of Graph
    Small_world_size = snap.GetMxScc(Small_world).GetEdges()
    print(Small_world_size)
    # Plot of Degree Distribution
    snap.PlotOutDegDistr(Small_world, "SmallWorldGraph", "Small World Degree Distribution")
    
    # Add Collaboration Network
    Collaboration_Network = snap.LoadEdgeList(snap.PUNGraph, "CA-HepTh.txt",0,1)
    snap.DelSelfEdges(Collaboration_Network)
    snap.PrintInfo(Collaboration_Network, "Graph Statistics", "info.txt", False)
    # Collaboration Network Clustering Coeffecient
    print("Clustering Coeffecient: ", clustering_coffecient(Collaboration_Network))
    # Diameter
    diameter_Collaboration_Network = snap.GetBfsEffDiamAll(Collaboration_Network, 10, False)
    print(diameter_Collaboration_Network[2])
    # Largest Strongly Connected Component
    print("Largest Strongly Connected Component - Maximum size:", snap.GetMxSccSz(Collaboration_Network))
    # Largest Size of Graph
    Collaboration_Network_size = snap.GetMxScc(Collaboration_Network).GetEdges()
    print(Collaboration_Network_size)
    # Plot of Degree Distribution
    snap.PlotOutDegDistr(Collaboration_Network, "CollaborationNetworkGraph", "Collaboration Network Degree Distribution")

main()
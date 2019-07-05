import snap
import matplotlib.pyplot as plt

"""def compute_modularity(G):
    
    if(G.GetEdges() > 0):
        edges = G.GetEdges()
        result = float(0.0)
        for i in G.Nodes():
            for j in G.Nodes():
                value = float(float(G.GetNI(i.GetId()).GetOutDeg()) * float(G.GetNI(j.GetId()).GetOutDeg()))
                value = float(float(value)/float(edge_weight))
                A = 0.0
                if (G.IsEdge(i.GetId(),j.GetId())):
                    A = 1.0
                value = float(A - value)
                result = result + value
        return result
    else:
        return 0"""
"""while(G.GetEdges > 0):
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    store_edge = []
    snap.GetBetweennessCentr(G, Nodes, Edges, 1.0)
    for edge in Edges:
        store_edge.append(Edges[edge])
    store_edge.sort(reverse=True)
    #print(store_edge[0])
    #NIdV = snap.TIntV()
    #for i in range(G.GetNodes()):
    #    NIdV.Add(i)
    #SubGraph.append(snap.GetSubGraph(G, NIdV))
    #l = len(SubGraph)
    #print("The number of components are ", l)
    array = []
    c = []
    for edge in Edges:
        if(Edges[edge] == store_edge[0]):
            G.DelEdge(edge.GetVal1(), edge.GetVal2())
            BfsTree1 = snap.GetBfsTree(G, edge.GetVal1(), True, False)
            BfsTree2 = snap.GetBfsTree(G, edge.GetVal2(), True, False)
            NIdV1 = snap.TIntV()
            NIdV2 = snap.TIntV()
            
            if(edge.GetVal1() not in array):
                for i in BfsTree1.Nodes():
                    NIdV1.Add(i.GetId())
                c.append(snap.GetSubGraph(G, NIdV1))
            if(edge.GetVal2() not in array):
                for i in BfsTree2.Nodes():
                    NIdV2.Add(i.GetId())
                c.append(snap.GetSubGraph(G, NIdV2))   
            array.append(edge.GetVal1())
            array.append(edge.GetVal2())
            #l1 = len(c) 
            #print("The Number of connected components are ", l1) 
    edge_weight = float(2 * G.GetEdges())   
    value_modularity = float(0.0)
    if(edge_weight > 0):
        for g in c:
            value_modularity = value_modularity + compute_modularity(g)
        value_modularity = float(float(value_modularity)/float(edge_weight))
    modularity.append((iterations,value_modularity))
    iterations = iterations + 1"""
    
#Load the edge list of the Karate dataset
G = snap.LoadEdgeList(snap.PUNGraph,"karateclub.txt",0,1)
# Now we need to keep a track of all the modularities
modularity = []
iterations = 0
# All the number of iterations that occur in removing edge betweenness
store_edge = []
value_modularity = float(0.0)
# Given that the modularity range is between [-1,1],
# We need to compare the values of every found modularity, 
# and at the maximum modularity, we shall output the community Structure
value_modularity_old = 1
for i in range(G.GetEdges()):
    edge_betweenness = float(0.0)
    source_node = float(0.0)
    dest_node = float(0.0)
    result = float(0.0)
    #Compute Edge Betweenness between edges to delete the edges
    edge_weight = float(2 * G.GetEdges())
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(G, Nodes, Edges, 1.0)
    # Compute node degree to be used in the Modularity 
    # Given that this is an undirected graph, in-degree = out-degree
    degree = snap.TIntV()
    snap.GetDegSeqV(G, degree)
    #Modularity = 1/2m(A - (k_i*k_j/2m))
    #A - represents edge weight between node i and node j
    #k_i and k_j are the sum of the weights of the edges attached to nodes i and j
    #2m - is the sum of all the edge weights in the graph
    for edge in Edges:
        if(edge_betweenness < Edges[edge]):
            edge_betweenness = Edges[edge]
            node_1 = edge.GetVal1()
            node_2 = edge.GetVal2()
        # Compute A - (k_i*k_j/2m) and keep on adding as per the formulae
        A = float(1.0)
        result = result + (A - ((degree[edge.GetVal1()-1])*(degree[edge.GetVal2()-1]))/(edge_weight))
    # Delete the edge which has the highest betweenness
    G.DelEdge(node_1,node_2)
    # Compute the modularity of the resultant graph
    value_modularity = float(result)/(edge_weight)
    # The process above is iterative in nature
    # It will keep on repeating until no more edges exists in the graph
    
    # Now we need to output the community structure for which the graph has highest modularity
    if(value_modularity == value_modularity_old):
        snap.DrawGViz(G, snap.gvlDot, "CommunityStructure.png", "Community Structure with Highest Modularity")
    iterations += 1
    
    # Keep a track of all the respective iterations recorded
    store_edge.append(i)
    # We shall record the values of all modularity after each iterations to plot a graph
    modularity.append(value_modularity)
    value_modularity_old = value_modularity
print(store_edge)
print(modularity)

# Now we need to print the graph of Modularity(y-axis) vs Iterations(x-axis)
plt.plot(store_edge,modularity)
plt.xlabel('Iterations')
plt.ylabel('Modularity')
plt.show()

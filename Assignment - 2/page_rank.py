import snap
import random
import matplotlib.pyplot as plt
import operator

def page_rank(G, b, e):
    node_array = []
    nodeid_array = []
    
    #As per the formulae we need to calculate '1/N'
    one_over_N = float(float(1)/float(G.GetNodes()))
    #print(one_over_N)
    for node in G.Nodes():
        node_id = node.GetId()
        nodeid_array.append(node_id)
        
        value_a = one_over_N
        value_b = node.GetOutDeg()
        node_array.append((value_a,value_b))
    
    #Page-Rank Implementation    
    while(True):
        temp = node_array
        for i, elem in enumerate(temp):
            node_id = nodeid_array[i]
            value_a,value_b = temp[i]
            curr_node = G.GetNI(node_id)
            x = curr_node.GetInDeg()
            
            if x != 0:
                total = 0
                for j in range(x):
                    in_node = curr_node.GetInNId(j)
                    out_degree = G.GetNI(in_node).GetOutDeg()
                    index_of_nodeid_array = nodeid_array.index(in_node)
                    in_b, in_c = temp[index_of_nodeid_array]
                    total = total + float(float(in_b)/float(out_degree))
                
                total = total * b
                temp[i] = (total,value_b)
                
            else:
                temp[i] = (0,value_b)
                
        sum_of_difference = 0
            
        for i,elem in enumerate(node_array):
            first_index, value_c = node_array[i]
            second_index, value_d = temp[i]
            difference = second_index - first_index
            sum_of_difference = sum_of_difference + difference
            
            
        if (sum_of_difference > e):  
            print(sum_of_difference)
            node_array = temp 
        else: 
            break
    return node_array

def main():
	#Loading the sample data of Epinions
    G = snap.LoadEdgeList(snap.PNGraph,"soc-Epinions1.txt",0,1)
    PR = page_rank(G, 0.8, 0.001)
    node_id = []
    
    for node in G.Nodes():
        node_id.append(node.GetId())
        
    temp1 = []
    temp2 = []
    
    for index,element in enumerate(PR):
        b,c = element
        temp1.append(b)
        temp2.append(node_id[index])
    
    temp1.sort(reverse=True)
    temp2.sort(reverse=True)
    
    #Finding top 10 IDs show casing with rank
    Nodes_top = temp1[0:10]
    Node_top_ids = temp2[0:10]
    print("Top 10 ranked nodes along with their ranks")
    print(Node_top_ids, Nodes_top)
    
    #Number of incoming edges for the top 10 and ranks of all source pages having hyper-links towards x
    print("Number of incoming edges (in-degree of x) and ranks of all the source pages having hyper-links toward x")
    for i, elem in enumerate(Node_top_ids):
         curr_node = G.GetNI(Node_top_ids[i])
         x = curr_node.GetInDeg()
         for j in range(x):
            in_node = curr_node.GetInNId(j)
            index = node_id.index(in_node)
            elem_ID = PR[index]
            print(Node_top_ids, in_node, x,elem_ID)
main()
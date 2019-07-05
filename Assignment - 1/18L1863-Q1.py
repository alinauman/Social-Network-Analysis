import snap

G = snap.LoadEdgeList(snap.PNGraph, "Wiki-Vote.txt",0,1)
snap.PrintInfo(G, "votes Stats", "votes-info.txt", False)

# Node ID with maximum degree
NId1 = snap.GetMxDegNId(G)
print("Node ID with Maximum-Degree: %d" % NId1)

# Number of Strongly connected components
ComponentDist = snap.TIntPrV()
snap.GetSccSzCnt(G, ComponentDist) 
for comp in ComponentDist:
    print("Size: %d - Number of Components: %d" % (comp.GetVal1(), comp.GetVal2()))

# Size of largest strongly connected component
print("Strongly Connected Component - Maximum size:", snap.GetMxSccSz(G))

# Number of Weakly Connected Components
CompDist = snap.TIntPrV()
snap.GetWccSzCnt(G, CompDist) 
for comp in CompDist:
    print("Size: %d - Number of Components: %d" % (comp.GetVal1(), comp.GetVal2()))

# Size of largest weakly connected component
print("Weakly Connected Component - Maximum size:", snap.GetMxWccSz(G))

# Plot of Outdegree Distribution
snap.PlotOutDegDistr(G, "Wiki Votes", "Wiki-Votes Out Degree")

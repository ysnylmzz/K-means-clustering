# # # ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## #   #
#  The Dunn Index is a method of evaluating clustering. A higher value is better.                                                       #
#  It is calculated as the lowest intercluster distance (ie. the smallest distance between any two cluster centroids) divided by        #
#  the highest intracluster distance (ie. the largest distance between any two points in any cluster).                                  #
# ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## #    #


# Function to find euclidean distance between two points 
def findDistance(point1, point2):
    
    eucDis = 0
    for i in range(len(point1)):
        eucDis = eucDis + (point1[i] - point2[i])**2
 
    return eucDis**0.5 

def calculateBCSS(cluster):
    bcss = []
    for count_cluster, cluster_center in enumerate(cluster): # for each cluster
        for count_cluster2, cluster_center2 in enumerate(cluster): # for each cluster
            if count_cluster !=count_cluster2:
                ddis = findDistance(cluster_center, cluster_center2)
                bcss.append(ddis)


    return sum(bcss)


# Function to calcualte Dunn Index
def calculateWCSS(points, cluster, labels):

    # points -- all data points
    # cluster -- cluster centroids
    wcss = []
    for count_cluster, cluster_center in enumerate(cluster): # for each cluster
        for count_point,p in enumerate(points): # for each point
            if labels[count_point] == count_cluster: #
                ddis = findDistance(cluster_center, p)
                wcss.append(ddis)



            
            
            # for t in points: # for each point
            #     if (t == p).all(): continue # if same point, ignore
            #     ddis = findDistance(t, p)
            # #    print('Denominator', denominator, ddis)
            #     denom = max(denom, ddis)
                
    return sum(wcss)


# Function to calcualte Dunn Index
def calcDunnIndex(points, cluster):

    # points -- all data points
    # cluster -- cluster centroids

    
    numer = float('inf')
    for c in cluster: # for each cluster
        for t in cluster: # for each cluster
           # print(t, c)
            if (t == c).all(): continue # if same cluster, ignore
            ndis = findDistance(t, c)
           # print('Numerator', numerator, ndis)
            numer = min(numer, ndis) # find distance between centroids
            
    denom = 0
    for c in cluster: # for each cluster
        for p in points: # for each point
            for t in points: # for each point
                if (t == p).all(): continue # if same point, ignore
                ddis = findDistance(t, p)
            #    print('Denominator', denominator, ddis)
                denom = max(denom, ddis)
                
    return numer/denom


import numpy as np
from sklearn.cluster import DBSCAN
import math

#clustering functions
def custom_metric(q, p, space_eps, time_eps):
    dist = 0
    for i in range(2):
        dist += (q[i] - p[i])**2
    spatial_dist = math.sqrt(dist)

    time_dist = math.sqrt((q[2]-p[2])**2)

    if time_dist/time_eps <= 1 and spatial_dist/space_eps <= 1 and p[3] != q[3]:
        return 1
    else:
        return 2


def doClustering(vector_4d, distance, time, minimum_cluster):

    params = {"space_eps": distance, "time_eps": time}
    db = DBSCAN(eps=1, min_samples=minimum_cluster-1, metric=custom_metric, metric_params=params).fit_predict(vector_4d)

    unique_labels = set(db)
    total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) -1

    print("Total clusters:", total_clusters)

    total_noise = list(db).count(-1)

    print("Total un-clustered:", total_noise)

    for k in unique_labels:
        if k != -1:

            labels_k = db == k
            cluster_k = vector_4d[labels_k]

            print("Cluster", k, " size:", len(cluster_k))

            for pt in cluster_k:
                print("(x:{}, y:{}, day:{}, caseNo:{})".format(pt[0], pt[1], pt[2], pt[3]))

            print()


# 5. manipulate the cluster function to print give the exact output the tasksheet requires.


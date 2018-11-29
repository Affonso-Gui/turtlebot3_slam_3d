# http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html

import sys
import yaml
import numpy as np

from sklearn.cluster import DBSCAN

# #############################################################################
# Read data
with open(sys.argv[1], "r") as input:
    array = []
    for line in input:
        coords = map(float, line.split('\t')[1:])
        array.append(coords)

X = np.array(array)

# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# #############################################################################
# Compute midpoints

with open("/home/nvidia/catkin_ws/src/darknet_ros/darknet_ros/config/yolov2.yaml", "r") as stream:
    yolo_classes = yaml.load(stream)['yolo_model']['detection_classes']['names']
    class_number = int(sys.argv[1][4:-4]) # out/24.txt
    class_name = yolo_classes[class_number]

label_types = set(labels)
if -1 in label_types: label_types.remove(-1)

with open("result.txt", "a+") as output:
    for k in label_types:
        class_member_mask = (labels == k)
        points = X[class_member_mask & core_samples_mask]
        mean = points.mean(axis=0)
        str = '{0} \t {1} \t {2} \t {3} \n'.format(class_name, mean[0], mean[1], mean[2])
        output.write(str)

# # #############################################################################
# # Plot result
# import matplotlib.pyplot as plt

# # Black removed and is used for noise instead.
# unique_labels = set(labels)
# colors = [plt.cm.Spectral(each)
#           for each in np.linspace(0, 1, len(unique_labels))]
# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise.
#         col = [0, 0, 0, 1]

#     class_member_mask = (labels == k)

#     xy = X[class_member_mask & core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
#              markeredgecolor='k', markersize=14)

#     mean = xy.mean(axis=0)
#     plt.plot(mean[0], mean[1], 'k+', markeredgewidth=2, markersize=10)

#     xy = X[class_member_mask & ~core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
#              markeredgecolor='k', markersize=6)

# plt.title('%s \n Estimated number of clusters: %d' % (sys.argv[1], n_clusters_))
# # plt.savefig('out/res/' + sys.argv[1][4:-4] + '.png') # sys.argv = out/24.txt
# plt.show()

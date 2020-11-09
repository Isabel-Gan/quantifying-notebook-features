import pandas as pd 
import csv
import numpy as np

# import kprotos ouptut
outliers_df = pd.read_pickle('full_reduced_outliers.pkl')
dists_df = pd.read_feather('prototypes-output/outliers_dists4.feather')
dists_df = dists_df.transpose()
clusters_df = pd.read_feather('prototypes-output/outliers_clusters4.feather')

# modify df to include cluster
outliers_df['cluster'] = clusters_df[['outliers_kprotos$cluster']].to_numpy()
outliers_df['cluster_dist'] = outliers_df['cluster']

# add distances (to all centers)
outliers_df[0] = dists_df[[0]].to_numpy()
outliers_df[1] = dists_df[[1]].to_numpy()
outliers_df[2] = dists_df[[2]].to_numpy()
outliers_df[3] = dists_df[[3]].to_numpy()

# center to specific cluster
outliers_df['cluster_dist'] = outliers_df['cluster_dist'].apply(lambda c : outliers_df[c - 1])

# drop the distance columns
outliers_df = outliers_df.drop([0, 1, 2, 3], axis = 1)

# output to pickle and csv
outliers_df.to_pickle('outliers_clusters.pkl')
outliers_df.to_csv('csv-files/outliers_clusters.csv')

# import data file
notebooks_df = pd.read_pickle('../full-dataset/notebooks.pkl')

# get the top notebooks
with open('top_notebooks.txt', 'w') as outfile:

    for cluster in range(1, 5):

        cluster_df = outliers_df[outliers_df['cluster'] == cluster]
        closest_notebooks = cluster_df.nsmallest(20, ['cluster_dist'])['nb_id'].to_list()

        closest_notebooks_df = notebooks_df[notebooks_df['nb_id'].isin(closest_notebooks)]

        outfile.write('------------- CLUSTER ' + str(cluster) + ' -------------------\n')
        outfile.write(closest_notebooks_df.to_string() + "\n")
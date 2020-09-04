import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
from termcolor import colored

# quantitative columns
quant_vars = ['jupyter_prop', 'output_cell_prop', 'markdown_prop', 'num_contrib', 'image_prop', 'md_frequency', 
                'num_commits', 'non_exec_prop', 'exec_inorder', 'exec_skips', 'num_functions', 'num_headers']

# categorical columns
cat_vars = ['longer_beginning', 'longer_ending', 'has_author', 'has_equation', 'is_education', 'has_links', 'has_comments', 
            'has_title', 'md_format', 'has_error', 'has_export', 'has_test', 'has_param']

# load in the dataframes
markdown_clusters_df = pd.read_csv('markdown_group_clusters.csv').drop(['Unnamed: 0'], axis = 1)
no_markdown_clusters_df = pd.read_csv('no_markdown_group_clusters.csv').drop(['Unnamed: 0'], axis = 1)

# for each cluster, generate graphs
for cluster in [0, 1, 2, 3]:

    cluster_df = no_markdown_clusters_df[no_markdown_clusters_df['cluster'] == cluster]
    
    outdir = 'no_md_graphs/cluster' + str(cluster) + '_graphs/'

    for feature in cluster_df.columns:

        # dont want to graph these columns
        if feature in ['nb_id', 'cluster']:
            continue 
            
        outfile = outdir + feature + str(cluster) + '.png'
        graph_title = feature + ' for cluster ' + str(cluster)

        # otws, we graph the feature depending on quant or cat
        plt.clf()
        if feature in quant_vars:
            plt.hist(cluster_df[feature])
            plt.title(graph_title)
            plt.savefig(outfile)
        elif feature in cat_vars:
            cat_plot = sns.countplot(x = feature, data = cluster_df)
            temp = cat_plot.set(title = graph_title)
            cat_plot.figure.savefig(outfile)
        
        # print success
        print(colored('generated graph for ' + feature + ' for cluster ' + str(cluster), 'green'))

# directory information

`binning-data/`: Jupyter notebook and .csv files of quantitative data binned 

`cluster-data/`: .csv files of notebook clusters and Jupyter notebook of cluster analyses

`figures/`: elbow graphs of clustering results

`rule-mining/`: .csv files of association rules and frequent itemsets and Jupyter notebook of analysis

# file information

`collect_data.py`: collects feature data across complete runs into `all_data.csv`

`all_data.csv`: all feature data across complete runs

`markdown_group.csv`: notebooks with markdown cells

`no_markdown_group.csv`: notebooks without markdown cells (with irrelevant features dropped)

`kproto-clustering.py`: performs k-prototypes clustering on mixed data to find the optimal number of clusters

`cat-factor-analysis.ipynb`: performs Multiple Correspondence Analysis and Association Rule Mining on the categorical (binned) data

`mixed-data-clustering.ipynb`: performs k-means and k-prototypes clustering on the data, extracting the optimal cluster centroids and labels

`mixed-data-factor-analysis.ipynb`: performs Principal Component Analysis, Factor Analysis for Mixed Data, and Multiple Factor Analysis on the data

`quant-var-analysis.ipynb`: performs Principal Component Analysis on the quantitative subset of the data (also performs filtering, cleaning, and grouping)

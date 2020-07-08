import pandas as pd
from kmodes.kprototypes import KPrototypes
import matplotlib.pyplot as plt

# load the data
md_df = pd.read_csv('markdown_group.csv')
no_md_df = pd.read_csv('no_markdown_group.csv')

# clear the first two columns in both groups
md_df = md_df.drop(['Unnamed: 0', 'nb_id'], axis = 1)
no_md_df = no_md_df.drop(['Unnamed: 0', 'nb_id'], axis = 1)

# perform k-prototypes clustering on markdown cell group
costs_md = []
K = range(1, 11)
for k in K:
    print("clustering with " + str(k) + " clusters")
    kproto = KPrototypes(n_clusters = k, init = 'Cao', n_jobs = 4, verbose = 0)
    clusters = kproto.fit_predict(md_df, categorical = [0, 1, 2, 3, 8, 9, 10, 12, 14, 18])
    costs_md.append(kproto.cost_)

# save the costs plot
plt.plot(K, costs_md, 'bx-')
plt.xlabel('k')
plt.ylabel('cost')
plt.title('Cost Graph for Optimal k for Markdown Cell Group')
plt.savefig('10-markdown-kproto.png')

# perform k-prototypes clustering on no markdown cell group
costs_no_md = []
K = range(1, 11)
for k in K:
    print("clustering with " + str(k) + " clusters")
    kproto = KPrototypes(n_clusters = k, init = 'Cao', n_jobs = 4, verbose = 0)
    clusters = kproto.fit_predict(no_md_df, categorical = [0, 4, 5, 10])
    costs_no_md.append(kproto.cost_)

# save the costs plot
plt.plot(K, costs_no_md, 'bx-')
plt.xlabel('k')
plt.ylabel('cost')
plt.title('Cost Graph for Optimal k for No Markdown Cell Group')
plt.savefig('10-no-markdown-kproto.png')
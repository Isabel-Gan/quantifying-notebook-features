import csv
import os
import pandas as pd

# repository data
repositories_path = 'full-dataset/repositories.csv'
repositories_df = pd.read_csv(repositories_path)

# path to the directory that holds all the notebooks
dataset_path = '../../../../DATA/jupyter_data/GITHUB_NOTEBOOKS_DATA/'

# dictionary row to write to the csv
row_write = {
    'nb_id': None,
    'repo_id': None,
    'name': None,
    'filepath': None
}

# path to the notebooks csv we will create
output_path = 'full-dataset/notebooks.csv'

# current ID
nb_id = 0

# number of notebooks to run for, if applicable
# limit = 20

# open the outfile
with open(output_path, 'w', newline='') as outcsv:

    # writes column headers
    writer = csv.DictWriter(outcsv, fieldnames = row_write.keys())
    writer.writeheader()

    # iterate through the repository dataframe
    for _, repository in repositories_df.iterrows():

        # get the repository id and name
        repo_id = repository['id']
        repo_name = repository['full name'] # don't need this, delete later

        # get the path that holds the notebooks
        repo_path = dataset_path + repo_name.replace('/', '~') + '_nb/'

        # try to get the repository path
        try:
            repo_files = os.listdir(repo_path)
        except FileNotFoundError:
            continue

        # iterate through the notebooks in the repo directory
        for file in repo_files:

            # assign a notebook id
            row_write['nb_id'] = nb_id

            # populate the notebook id
            row_write['repo_id'] = repo_id 

            # get the filename and check that it is a notebook
            filename = os.fsdecode(file)
            if '.ipynb' in filename:
                row_write['name'] = filename 
            else:
                continue 

            # get the path to the notebook
            row_write['filepath'] = repo_name.replace('/', '~') + '_nb/' + filename

            # write the row to the csv and iterate notebook IDs
            writer.writerow(row_write)
            nb_id += 1
            print("wrote notebook " + filename)

            # check counter
            # if nb_id == limit:
            #     break
        
        # check counter
        # if nb_id == limit:
        #     break

        print("wrote repository " + repo_name)
        
    print("finished! successfully loaded " + str(nb_id) + " notebooks")

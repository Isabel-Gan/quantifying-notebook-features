import pandas as pd
import json

df_nb = pd.read_csv('test-dataset/notebooks_sample.csv')

# uses the csv file to find the corresponding repository id given a notebook id
def get_repo_id(nb_id):
    nb_row = df_nb.loc[df_nb['nb_id'] == nb_id]
    return int(nb_row['repo_id'])

# given a notebook id, returns the metadata (as a python dictionary object) of its repository
def get_repo_metadata(nb_id):

    # get the file path
    repo_id = get_repo_id(nb_id)
    repo_meta_file = 'test-dataset/repository_metadata/repo_' + str(repo_id) + '.json'

    # try to load the file
    with open(repo_meta_file) as meta_file:
        try:
            return json.load(meta_file)
        except:
            return None

# given a notebook id, returns the notebook file as a python dictionary object
def get_nb(nb_id):

    # get the file path
    nb_file = 'test-dataset/notebooks/nb_' + str(nb_id) + '.ipynb'

    # try to load the file
    with open(nb_file) as nb_file:
        try:
            return json.load(nb_file)
        except:
            return None

# given a notebook id, returns the cells in the notebook as a python list
def get_cells(nb_id):

    # get the notebook file
    nb = get_nb(nb_id)

    # get the cells
    keys = nb.keys()
    if 'cells' in keys:
        return nb['cells']
    elif 'worksheets' in keys:
        return nb['worksheets'][0]['cells']
    else:
        return None

# prints a json file, but nice
def print_json(json_file):
    print(json.dumps(json_file, indent=4))

# tests - delete later

import pandas as pd
import json
from GitHubAPI_Crawler.github_api import GitHubAPI

api = GitHubAPI()
df_nb = pd.read_csv('test-dataset/notebooks_sample.csv')

''' api access '''

# strips the github api url down to just the path so it works with the api crawler
def strip_url(url):
    new_url = url.replace("https://api.github.com/", "")
    return new_url

''' file access '''

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

''' repo access '''

# returns the languages used in the repo of the notebook as a python dictionary object
def get_languages(nb_id):

    # open the metadata file
    repo_meta = get_repo_metadata(nb_id)

    # get the url and access api to get the data
    languages_url = repo_meta['languages_url']
    response = api.request(strip_url(languages_url))

    return response

# returns the data of the owner of the repo as a python dictionary object
def get_owner(nb_id):

    # open the metadata file
    repo_meta = get_repo_metadata(nb_id)

    # return the correct field
    return repo_meta['owner']

# returns the data from the url of the owner of the repo as a python dictionary object
def get_owner_url(nb_id):

    # get the owner data
    owner_data = get_owner(nb_id)

    # get the url and access api to get the data
    owner_url = owner_data['url']
    response = api.request(strip_url(owner_url))

    return response

''' notebook access'''

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

# given a notebook id, returns the markdown cells as a python list
def get_md_cells(nb_id):

    # get the cells 
    cells = get_cells(nb_id)

    # filter down to only markdown cells
    md_cells = filter(lambda cell: cell['cell_type'] == "markdown", cells)
    return md_cells

''' misc '''

# prints a json file, but nice
def print_json(json_file):
    print(json.dumps(json_file, indent=4))

# tests - delete later

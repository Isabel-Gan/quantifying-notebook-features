import pandas as pd
import json
from GitHubAPI_Crawler.github_api import GitHubAPI
from comment_parser import comment_parser

import notebook_analysis as nb_analysis

api = GitHubAPI()

# the dataset directory should have two directories: notebooks and repository_metadata
# dataset_directory = '../../../../DATA/jupyter_data/GITHUB_2017_DATASET/sample_data/data/'
dataset_directory = 'test-dataset/'

# the csv directory should have at least the notebooks_sample.csv file
# csv_directory =  '../../../../DATA/jupyter_data/GITHUB_2017_DATASET/sample_data/data/csv/'
csv_directory = 'test-dataset/'

# load the csv file
nb_csv_path = csv_directory + 'notebooks_sample.csv'
df_nb = pd.read_csv(nb_csv_path)

''' api access '''

# strips the github api url down to just the path so it works with the api crawler
def strip_url(url):
    new_url = url.replace("https://api.github.com/", "")
    return new_url

# returns the data from the given user url as a python dictionary object
def get_url(url):
    response = api.request(strip_url(url))
    return response

''' file access '''

# uses the csv file to find the corresponding field given a notebook id
def get_csv_field(field, nb_id):
    nb_row = df_nb.loc[df_nb['nb_id'] == nb_id]
    return nb_row[field]

# uses the csv file to find the corresponding repository id given a notebook id
def get_repo_id(nb_id):
    return int(get_csv_field('repo_id', nb_id))

# uses the csv file to find the corresponding file name given a notebook id
def get_nb_name(nb_id):
    return str(get_csv_field('name', nb_id))

# uses the csv file to find the corresponding path given a notebook id
def get_path(nb_id):
    return str(get_csv_field('path', nb_id))

# given a notebook id, returns the metadata (as a python dictionary object) of its repository
def get_repo_metadata(nb_id):

    # get the file path
    repo_id = get_repo_id(nb_id)
    repo_meta_file = dataset_directory + 'repository_metadata/repo_' + str(repo_id) + '.json'

    # try to load the file
    with open(repo_meta_file) as meta_file:
        try:
            return json.load(meta_file)
        except:
            return None

# given a notebook id, returns the notebook file as a python dictionary object
def get_nb(nb_id):

    # get the file path
    nb_file = dataset_directory + 'notebooks/nb_' + str(nb_id) + '.ipynb'

    # try to load the file
    with open(nb_file) as nb_file:
        try:
            return json.load(nb_file)
        except:
            return None

''' repo access '''

# returns the resulting python object from requesting the api at the given repository field
def get_repo_field(nb_id, field):

    # open the metadata file
    repo_meta = get_repo_metadata(nb_id)

    # get the url and access the api to get the data
    url = repo_meta[field]
    response = api.request(strip_url(url))

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

        # go through each worksheet and return all cells
        total_cells = []
        for cell_group in nb['worksheets']:
            total_cells += cell_group['cells']
        
        return total_cells
        
    else:
        return None

# given a notebook id, returns the markdown cells as a python list
def get_md_cells(nb_id):

    # get the cells 
    cells = get_cells(nb_id)

    # filter down to only markdown cells
    md_cells = filter(lambda cell: cell['cell_type'] == "markdown", cells)
    return list(md_cells)

# given a notebook id, returns the code cells as a python list
def get_code_cells(nb_id):

    # get the cells
    cells = get_cells(nb_id)

    # filter down to only code cells
    code_cells = filter(lambda cell: cell['cell_type'] == "code", cells)
    return list(code_cells)

# given a notebook id, returns all comments in code as a python list of strings
def get_comments(nb_id):
    
    # check if notebook is in python
    language = nb_analysis.get_language(nb_id)
    if language == None or "python" not in nb_analysis.get_language(nb_id):
        return None

    # get the code cells
    code_cells = get_code_cells(nb_id)

    # iterate through the code cells and gather the comments
    comments = []
    for cell in code_cells:

        # look for the field that holds the code
        field = ""
        if 'input' in cell.keys():
            field = 'input'
        elif 'source' in cell.keys():
            field = 'source'
        

        # gather all of the code into a single string
        code = str("".join(cell[field]))

        # get the comments
        try:
            comments += list(map(lambda x : x.text(), comment_parser.extract_comments_from_str(code, mime='text/x-python')))
        except:
            # the comment parser will not work on syntactically incorrect code
            continue

    return comments

''' misc '''

# prints a json file, but nice
def print_json(json_file):
    print(json.dumps(json_file, indent=4))

# tests - delete later

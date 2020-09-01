import pandas as pd
import json
from GitHubAPI_Crawler.github_api import GitHubAPI
from comment_parser import comment_parser
import api_cache

import notebook_analysis as nb_analysis

dbg_print = lambda x : x

api = GitHubAPI()

# load the notebooks csv file
nb_df = pd.read_pickle('full-dataset/notebooks.pkl')

# load the repositories csv file
repo_df = pd.read_pickle('full-dataset/repositories.pkl')

# path to dataset
dataset_path = '../../../../DATA/jupyter_data/GITHUB_NOTEBOOKS_DATA/'
repos_path = '../../../../DATA/jupyter_data/GITHUB_NOTEBOOKS_REPO_METADATA/'
owners_path = '../../../../DATA/jupyter_data/GITHUB_NOTEBOOKS_REPO_OWNERS/'

''' api access '''

# strips the github api url down to just the path so it works with the api crawler
def strip_url(url):
    new_url = url.replace("https://api.github.com/", "")
    return new_url

# returns the data from the given user url as a python dictionary object
def get_url(url):
    # check if in cache already
    response = api_cache.is_in_cache(url)
    if response != None:
        return response
    
    # not in cache
    response = api.request(strip_url(url))
    api_cache.add_to_cache(url, response)
    return response

''' file access '''

# uses the csv files to find the corresponding field given a notebook id
def get_csv_field(field, nb_id):
    nb_row = nb_df.loc[nb_df['nb_id'] == nb_id]
    return nb_row[field]

# uses the csv file to find the corresponding repository id given a notebook id
def get_repo_id(nb_id):
    return int(get_csv_field('repo_id', nb_id).item())

# uses the csv file to find the corresponding file name given a notebook id
def get_nb_name(nb_id):
    return str(get_csv_field('nb_name', nb_id).item())

# uses the csv file to find the corresponding path given a notebook id
def get_path(nb_id):
    return str(get_csv_field('nb_path', nb_id).item())

# uses the csv file to find the corresponding filepath given a notebook id
def get_filepath(nb_id):
    return str(get_csv_field('filepath', nb_id).item())

# given a notebook id, returns the metadata (as a python dictionary object) of its repository
def get_repo_metadata(nb_id):

    # get the file path
    repo_id = get_repo_id(nb_id)
    repo_row = repo_df.loc[repo_df['id'] == repo_id].iloc[0]
    repo_name = repo_row['full name']
    filename = str(repo_id) + '_' + (repo_name.replace('/', '~')) + '.json'

    # get the metadata file
    with open(repos_path + filename, 'r') as meta_file:
        try:
            return json.load(meta_file)
        except:
            return None

# given a notebook id, returns the notebook file as a python dictionary object
def get_nb(nb_id):

    # get the file path
    nb_file = dataset_path + get_filepath(nb_id)

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
    dbg_print(url)

    # check cache
    response = api_cache.is_in_cache(url)
    if response != None:
        return response

    # not in cache
    response = api.request(strip_url(url))
    api_cache.add_to_cache(url, response)
    return response

# returns the data of the owner of the repo as a python dictionary object
def get_owner(nb_id):

    # open the metadata file
    repo_meta = get_repo_metadata(nb_id)

    # return the correct field
    return repo_meta['owner']

# returns the data from the url of the owner of the repo as a python dictionary object
def get_owner_url(nb_id):

    # get the owner name
    owner_name = get_owner(nb_id)['login']

    # get the owner url response from file
    owner_filepath = owners_path + owner_name + '.json'
    with open(owner_filepath, 'r') as owner_file:
        try:
            return json.load(owner_file)
        except:
            return None

# returns the usernames of the authors as a python list from the csv
def get_authors(nb_id):

    #  get the row of the dataframe
    repo_id = get_repo_id(nb_id)
    repo = repo_df.loc[repo_df['id'] == repo_id].squeeze()

    # return the authors for the repo
    return repo['authors']

# returns the commits to a repo that affect the notebook file specifically
def get_nb_commits(nb_id):

    # get notebook path
    nb_path = get_path(nb_id)

    # get commit url
    repo_metadata = get_repo_metadata(nb_id)
    url_template = repo_metadata['commits_url']

    # change the url to be specific to the notebook
    nb_commit_url = url_template.replace("{/sha}", "?path=" + nb_path).replace('%', '%25')
    
    # query the api to the url (we don't check the cache, since this will always be unique)
    response = api.request(strip_url(nb_commit_url))
    return response

# retrieves the files in the directory of the notebook in the repository
def get_files(nb_id):

    dbg_print(nb_id)

    # get notebook path
    nb_path = get_path(nb_id)

    # get notebook name and replace it in the path
    nb_name = get_nb_name(nb_id)
    dbg_print(nb_name)
    nb_path = nb_path.replace(nb_name, '')
    dbg_print(nb_path)

    # get the content url for the directory
    repo_metadata = get_repo_metadata(nb_id)
    nb_dir_url = repo_metadata['contents_url'].replace("{+path}", nb_path).replace('%', '%25')

    dbg_print(nb_dir_url)

    # query the api to the url, check the cache first
    response = api_cache.is_in_cache(nb_dir_url)
    if response != None:
        return response 

    # not in cache
    response = api.request(strip_url(nb_dir_url))
    api_cache.add_to_cache(nb_dir_url, response)
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

# given a notebook id, returns the markdown cell groups as a python list
def get_md_groups(nb_id):

    # get the cells
    cells = get_cells(nb_id)

    # iterate through and gather the groups
    groups = []
    group = []

    for cell in cells:
        if cell['cell_type'] == "markdown":
            group.append(cell)
        elif group != []:
            groups.append(group)
            group = []
    
    # add the last markdown group (if the last cell was a markdown cell)
    if group != []:
        groups.append(group)
    
    return groups
        
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
        keys = cell.keys()
        if 'input' in keys:
            field = 'input'
        elif 'source' in keys:
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
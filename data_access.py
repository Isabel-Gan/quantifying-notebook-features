import pandas as pd
import json
from GitHubAPI_Crawler.github_api import GitHubAPI
from comment_parser import comment_parser

import notebook_analysis as nb_analysis

api = GitHubAPI()

# the dataset directory should have two directories: notebooks and repository_metadata
# dataset_directory = '../../../../DATA/jupyter_data/GITHUB_2017_DATASET/sample_data/data/'
# dataset_directory = 'test-dataset/'
dataset_directory = '../research-dataset/sample_data/data/'

# the csv directory should have at least the notebooks_sample.csv file
# csv_directory =  '../../../../DATA/jupyter_data/GITHUB_2017_DATASET/sample_data/data/csv/'
# csv_directory = 'test-dataset/'
csv_directory = '../research-dataset/sample_data/data/csv/'

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
    return int(get_csv_field('repo_id', nb_id).item())

# uses the csv file to find the corresponding file name given a notebook id
def get_nb_name(nb_id):
    return str(get_csv_field('name', nb_id).item())

# uses the csv file to find the corresponding path given a notebook id
def get_path(nb_id):
    return str(get_csv_field('path', nb_id).item())

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

# returns the commits to a repo that affect the notebook file specifically
def get_nb_commits(nb_id):

    # get notebook path
    nb_path = get_path(nb_id)

    # get commit url
    repo_metadata = get_repo_metadata(nb_id)
    url_template = repo_metadata['commits_url']

    # change the url to be specific to the notebook
    nb_commit_url = url_template.replace("{/sha}", "?path=" + nb_path)
    
    # query the api to the url
    response = api.request(strip_url(nb_commit_url))
    return response

# retrieves the files in the directory of the notebook in the repository
def get_files(nb_id):

    # get notebook path
    nb_path = get_path(nb_id)

    # get notebook name and replace it in the path
    nb_name = get_nb_name(nb_id)
    nb_path = nb_path.replace(nb_name, '')

    # get the content url for the directory
    repo_metadata = get_repo_metadata(nb_id)
    nb_dir_url = repo_metadata['contents_url'].replace("{+path}", nb_path)

    # query the api to the url
    response = api.request(strip_url(nb_dir_url))
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

''' owner information '''

# given a notebook id, gets the number of repos owned by the users
def get_repos(nb_id):

    # get the owner information
    user_info = get_owner_url(nb_id)

    # get the list of repos
    user_repos_url = user_info['repos_url']
    user_repos = api.request(strip_url(user_repos_url))

    return user_repos

# given a notebook id, gets the number of repos
def get_num_projects(nb_id):

    # get the owner's repos
    user_repos = get_repos(nb_id)

    return len(user_repos)

# given a notebook id, gets the number of data science repos
def get_num_ds_projects(nb_id):

    # get the owner's repos
    user_repos = get_repos(nb_id)

    # returns true if a repo is in Jupyter Notebook
    def is_jn(repo):

        # get languages info
        languages_url = repo['languages_url']
        languages_info = api.request(strip_url(languages_url))

        # iterate through languages, get the highest one
        max_language_num = 0
        max_language = None
        for language in languages_info:
            if languages_info[language] > max_language_num:
                max_language_num = languages_info[language]
                max_language = language

        # check if Jupyter Notebook top language
        return (max_language == "Jupyter Notebook")

    # filter the list of repos
    ds_repos = filter(is_jn, user_repos)
    return len(ds_repos)

# gets the number of followers for the owner of a notebook
def get_num_followers(nb_id):

    # get owner information
    user_info = get_owner_url(nb_id)

    # get followers info
    followers_url = user_info['followers_url']
    followers = api.request(strip_url(followers_url))

    return len(followers)

# gets the number of years a notebook owner's account has been active
def get_account_age(nb_id):

    # get the owner information
    user_info = get_owner_url(nb_id)

    # get the year of account creation
    created_date = user_info['created_at']
    created_year = int(created_date[:4])

    return (2021 - created_year)

''' misc '''

# prints a json file, but nice
def print_json(json_file):
    print(json.dumps(json_file, indent=4))

# tests - delete later

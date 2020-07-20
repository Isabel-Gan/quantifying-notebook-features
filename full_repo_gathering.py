import pandas as pd 
import json
import termcolor
from GitHubAPI_Crawler.github_api import GitHubAPI

# api
api = GitHubAPI()

# repositories dataframe
repositories_df = pd.read_pickle('full-dataset/repositories.pkl')

# output directory for repo metadata
output_dir = '../GITHUB_NOTEBOOKS_REPO_METADATA/'

# for each repository
for _, repo in repositories_df.iterrows():

    # get repo name and id
    repo_name = repo['full name']
    repo_id = repo['id']

    # query the api to get the metadata
    try:
        metadata = api.request('repos/' + repo_name)
    except:
        print(colored('could not get metadata for repo ' + str(repo_id) + ', ' + repo_name, 'red'))

    # output the metadata to a file
    filename = str(repo_id) + '_' + (repo_name.replace('/', '~')) + '.json'
    with open(output_dir + filename, 'w') as outfile:
        json.dump(metadata, outfile)
        print('got metadata for repo ' + str(repo_id) + ', ' + repo_name)
import pandas as pd 
import json
from termcolor import colored
import sys
from GitHubAPI_Crawler.github_api import GitHubAPI

# generates a certain number of segments
def get_segments(num_segments):
    
    # segment properties
    total_repos = 29820
    segments = []
    segment_size = int(total_repos / num_segments)

    # generate each segment
    prev_end = None
    for i in range(num_segments):

        if prev_end == None:
            segments.append((0, segment_size))
            prev_end = segment_size 
        elif i == num_segments - 1:
            segments.append((prev_end + 1, total_repos - 1))
        else:
            new_end = (prev_end + 1) + segment_size
            segments.append((prev_end + 1, new_end))
            prev_end = new_end

    return segments

# get the number of segments we want
segments = get_segments(4)
segment_num = int(sys.argv[1])
cur_segment = segments[segment_num]

# api
api = GitHubAPI()

# repositories dataframe
repositories_df = pd.read_pickle('full-dataset/repositories.pkl')

# output directory for repo metadata
output_dir = '../../../../DATA/jupyter_data/GITHUB_NOTEBOOKS_REPO_OWNERS/'

# counter and limit, if applicable
# limit = 20
# counter = 0

# previous repository owner
prev_owner = None

# for each repository
for _, repo in repositories_df.iloc[cur_segment[0]:cur_segment[1] + 1].iterrows():

    # get owner name
    repo_name = repo['full name']
    repo_owner = repo_name.split('/')[0]

    # check the previous owner
    if prev_owner == None or prev_owner != repo_owner:
        # first or new owner
        prev_owner = repo_owner
    elif prev_owner == repo_owner:
        # same owner
        continue

    # query the api to get the metadata
    try:
        metadata = api.request('users/' + repo_owner)
    except:
        print(colored('could not get metadata for repo ' + str(repo_id) + ', ' + repo_name, 'red'))
        continue

    # output the metadata to a file
    filename = repo_owner + '.json'
    with open(output_dir + filename, 'w') as outfile:
        json.dump(metadata, outfile)
        print('got owner data for ' + repo_owner)

        # iterate and check counter
        # counter += 1
        # if counter == limit:
        #     break

print(colored('finished! successfully finished segment ' + str(segment_num), 'green'))
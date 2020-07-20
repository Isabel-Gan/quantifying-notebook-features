import full_data_access as data   

''' feature - other files that are non-Jupyter '''

# calculates the proportion of code in the repo written in jupyter
def jupyter_prop(nb_id):

    # get the language data
    languages_data = data.get_repo_field(nb_id, 'languages_url')
    keys = languages_data.keys()

    # check if language data is recorded and jupyter notebook is part of it
    if 'Jupyter Notebook' in keys:

        # calculate the sum of bytes of code in the repo
        bytes_sum = 0
        for key in keys:
            bytes_sum += languages_data[key]
        
        # calculate the proportion of code in jupyter
        bytes_jupyter = languages_data['Jupyter Notebook']
        return float(bytes_jupyter) / float(bytes_sum)

    # if language data not recorded/jupyter notebook not in data
    else:
        return None

''' feature - contributors '''

# returns the number of contributors to a notebook's repository
def num_contributors(nb_id):

    # get the data
    contrib_meta = data.get_repo_field(nb_id, 'contributors_url')

    # count number of contributors in the object and return
    return len(contrib_meta)

# tests - delete later

''' feature - use of version control '''

# returns the number of commits to the repository applying to a notebook
def num_commits(nb_id):

    # get commits to the notebook
    commits = data.get_nb_commits(nb_id)

    return len(commits)

''' feature - notebook commit messages '''

# returns the commit messages related to the notebook as a python list
def get_commit_messages(nb_id):

    # get commits to the notebook
    commits = data.get_nb_commits(nb_id)

    # map each commit to its message 
    commit_msgs = list(map(lambda commit : commit['commit']['message'], commits))

    return list(commit_msgs)

''' feature - manage dependencies and imports '''

# checks if there is a requirements.txt in the same directory as the notebook
def has_requirements(nb_id):

    # get the files in the notebook directory
    dir_files = data.get_files(nb_id)

    # check the files for requirements.txt
    for file in dir_files:
        if file['name'] == 'requirements.text':
            return True 
    
    return False

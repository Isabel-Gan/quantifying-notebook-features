import pandas as pd
import csv
import os
import subprocess
import re
from termcolor import colored

# segments of notebooks (for parallelization)
segments = [(0, 35781), (35782, 71562), (71563, 107343), (107344, 143124)]
segment_num = 0
cur_segment = segments[segment_num]

# load the notebooks csv
nb_filepath = 'full-dataset/notebooks.csv'
nb_df = pd.read_csv(nb_filepath)

# load the repositories csv
repo_filepath = 'full-dataset/repositories.csv'
repo_df = pd.read_csv(repo_filepath)

# python dictionary for rows
row_write = {
    'nb_id' : None,
    'nb_path' : None
}

# output for this segment
output_path = 'full-dataset/nb_paths_segment' + str(segment_num) + '.csv'
output_error_path = 'full-dataset/errors_segment' + str(segment_num) + '.txt'

# will hold ongoing repo name and whether or not it errored
prev_repo_name = (None, None)

# clones a repository, raising an exception if it cannot be cloned
def clone_repo(repo_full_name, error_file):

    try:
        # try to clone the repo
        print(colored('cloning ' + repo_full_name + '...', 'cyan'))
        subprocess.run(["git", "clone", "https://github.com/" + repo_full_name], timeout = 300)

        # clone successful
        print(colored("successfully cloned " + repo_full_name, 'cyan'))
        return True

    except subprocess.TimeoutExpired:
        # delete the folder created for the repo
        repo_name = repo_full_name.split('/')[1]
        subprocess.run(["rm", "-rf", repo_name])

        # error output
        output_msg = 'could not clone ' + repo_full_name + ', timed out'
        print(colored(output_msg, 'red'))
        error_file.write(output_msg + '\n')
        return False

    except:
        # error output
        output_msg = 'could not clone ' + repo_full_name
        print(colored(output_msg, 'red'))
        error_file.write(output_msg + '\n')
        return False

# open the outfile
with open(output_path, 'w', newline='') as outcsv, open(output_error_path, 'w') as error_file:

    # writes column headers
    writer = csv.DictWriter(outcsv, fieldnames = row_write.keys())
    writer.writeheader()

    # destination directory for temporarily cloning the repositories
    temp_dir = '/home/feature/igan/quantifying-notebook-features/temp/temp' + str(segment_num) + '/'
    os.chdir(temp_dir)

    # iterate through each notebook
    for nb_id in range(cur_segment[0], cur_segment[1] + 1):

        # get notebook row and assign notebook id
        notebook = nb_df.loc[nb_df['nb_id'] == nb_id]
        row_write['nb_id'] = nb_id

        # get notebook name
        nb_name = str(notebook['name'].item())

        # get repository name 
        repo_id = int(notebook['repo_id'].item())
        repo_row = repo_df.loc[repo_df['id'] == repo_id].iloc[0]
        repo_full_name = repo_row['full name']
        repo_name = repo_full_name.split('/')[1]

        # check previous repo name
        if prev_repo_name[0] == None:

            try:
                # try to clone the repo
                result = clone_repo(repo_full_name, error_file)

                # first repository
                prev_repo_name = (repo_name, result)

                # go into the folder
                if result:
                    os.chdir(temp_dir + repo_name)
                else:
                    raise Exception('couldn\'t clone repo')
            except:
                error_file.write('notebook ' + str(nb_id) + '\n')
                continue

        elif repo_name != prev_repo_name[0]:

            # delete the previous repo 
            os.chdir(temp_dir)
            subprocess.run(["rm", "-rf", temp_dir + prev_repo_name[0]])

            try:
                # try to clone the repo
                result = clone_repo(repo_full_name, error_file)

                # update prev_repo
                prev_repo_name = (repo_name, result)

                # go into the folder
                if result:
                    os.chdir(temp_dir + repo_name)
                else:
                    raise Exception('couldn\'t clone repo')
            except:
                error_file.write('notebook ' + str(nb_id) + '\n')
                continue

        elif repo_name == prev_repo_name[0]:

            # check result
            if prev_repo_name[1]:
                # go into folder
                try:
                    os.chdir(temp_dir + repo_name)
                except FileNotFoundError:
                    error_file.write('notebook ' + str(nb_id) + ', repo not found' + '\n')
                    continue
            else:
                error_file.write('notebook ' + str(nb_id) + '\n')
                continue

        # generate the tree and iterate through the files
        p = subprocess.Popen('git ls-tree -r master --name-only', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            line = str(line)

            # isolate filepath in the line
            line = line.split("'")[1]
            line = line.split("\\")[0]
            filepath = line

            # isolate the file in the filepath
            filename = filepath.split('/')[-1]

            # check the filename against the notebook name
            if filename == nb_name:
                nb_path = filepath
                break

        # assign notebook path and write row
        row_write['nb_path'] = nb_path 
        writer.writerow(row_write)
        print(colored("found path " + str(nb_path), 'green'))
    
    print(colored("successfully finished segment " + str(segment_num), 'green'))
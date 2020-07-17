import pandas as pd
import csv
import os
import subprocess
import re
from termcolor import colored

# segments of notebooks (for parallelization)
segments = [(0, 35781), (35782, 71562), (71563, 107343), (107344, 143124)]
segment_num = 3
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

# counter and limit
counter = 0
limit = 20

# open the outfile
with open(output_path, 'w', newline='') as outcsv:

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
        repo_row = repo_df.loc[repo_df['id'] == repo_id]
        repo_full_name = str(repo_row['full name'].item())
        repo_name = repo_full_name.split('/')[1]

        # clone the repo and go into folder
        subprocess.run(["git", "clone", "https://github.com/" + repo_full_name])
        os.chdir(temp_dir + repo_name)

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

        # delete the repo
        os.chdir(temp_dir)
        subprocess.run(["rm", "-rf", temp_dir + repo_name])
            
        # assign notebook path and write row
        row_write['nb_path'] = nb_path 
        writer.writerow(row_write)
        print(colored("found path " + str(nb_path), 'green'))

        # iterate and check counter
        counter += 1
        if counter == limit:
            break
    
    print(colored("successfully finished segment " + str(segment_num), 'green'))
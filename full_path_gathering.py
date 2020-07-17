import pandas as pd
import csv
import full_data_access as data

# segments of notebooks (for parallelization)
segments = [(0, 35781), (35782, 71562), (71563, 107343), (107344, 143124)]
segment_num = 3
cur_segment = segments[segment_num]

# recursively searches a list of files or directories for the notebook, appending path 
def search(target, files):

    # go through each file
    for file in files:

        # check file type
        file_type = file['type']

        # if a directory, recurse
        if file_type == 'dir':
            
            # get the files in the directory
            dir_files = data.get_url(file['url'])

            # recurse
            rec_res = search(target, dir_files)
            if rec_res != None:
                return rec_res

        # if a file, check the filename
        elif file_type == 'file':
            if file['name'] == target:
                return file['path']
            
    # not found in this set of files
    return None

# load the notebooks csv
nb_filepath = 'full-dataset/notebooks.csv'
nb_df = pd.read_csv(nb_filepath)

# python dictionary for rows
row_write = {
    'nb_id' : None,
    'nb_path' : None
}

# output for this segment
output_path = 'full-dataset/nb_paths_segment' + str(segment_num) + '.csv'

# open the outfile
with open(output_path, 'w', newline='') as outcsv:

    # writes column headers
    writer = csv.DictWriter(outcsv, fieldnames = row_write.keys())
    writer.writeheader()

    # iterate through each notebook
    for nb_id in range(cur_segment[0], cur_segment[1] + 1):

        # get notebook row and assign notebook id
        notebook = nb_df.loc[nb_df['nb_id'] == nb_id]
        row_write['nb_id'] = nb_id

        # get notebook name
        nb_name = str(notebook['name'].item())

        # get the repo metadata of the notebook
        repo_metadata = data.get_repo_metadata(nb_id)

        # get the contents of the repo
        try:
            # get the contents of the repo
            contents_url = repo_metadata['contents_url'].replace('{+path}', '')
            all_files = data.get_url(contents_url)

            # search for the notebook in the path
            nb_path = search(nb_name, all_files)
        except:
            # probably a 404 
            nb_path = None
            
        # assign notebook path and write row
        row_write['nb_path'] = nb_path 
        writer.writerow(row_write)

        print("found path " + str(nb_path))
    
    print("successfully finished segment " + str(segment_num))
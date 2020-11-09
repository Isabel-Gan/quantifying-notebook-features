import pandas as pd 
import csv
from termcolor import colored
import numpy as np

# row for writing to the existing results df
row = {
    'nb_id' : None,
    'repo_id' : None,
    'longer_beginning' : None,
    'longer_ending' : None,
    'has_author' : None,
    'has_equation' : None,
    'jupyter_prop' : None,
    'output_cell_prop' : None,
    'markdown_prop' : None,
    'num_contrib' : None,
    'image_prop' : None,
    # 'e_keywords' : None,
    # 'p_keywords' : None,
    # 's_keywords' : None,
    'is_education' : None,
    'language' : None,
    'has_links' : None,
    'has_comments' : None,
    'md_frequency' : None,
    'has_title' : None,
    'num_commits' : None,
    'md_format' : None,
    'non_exec_prop' : None,
    'exec_inorder' : None,
    'exec_skips' : None,
    'has_error' : None,
    # 'comm_messages' : None,
    'speaking_language' : None,
    'has_export' : None,
    'num_functions' : None,
    'has_test' : None,
    'num_headers' : None,
    'has_param' : None,
    'has_reqtext' : None,
    'num_stars' : None,
    'errors' : None
}

# dataframes
results_df = pd.read_csv('complete-runs/second-run.csv')
errors_df = pd.read_csv('complete-runs/second-errors.csv')

notebooks_df = pd.read_pickle('../full-dataset/notebooks.pkl')

# add errors column to results
results_df['errors'] = np.nan

# for each notebook, check if in errors and write to results
for _, notebook in notebooks_df.iterrows():

    # get notebook id and repository id
    nb_id = notebook['nb_id'] 
    repo_id = notebook['repo_id']

    # look in the errors for the notebook
    error_row = errors_df.loc[errors_df['nb_id'] == nb_id]

    # if not empty, write to the column
    if not error_row.empty:

        # write the error(s)
        error = ''
        for _, err_row in error_row.iterrows():
            error += err_row['err_in'] + ','
        error = error[:-1]
        
        # look for the row in the results df
        results_row = results_df.loc[results_df['nb_id'] == nb_id]

        # if empty, we have to write a new row
        if results_row.empty:
            row['nb_id'] = nb_id
            row['repo_id'] = repo_id
            row['errors'] = error
            results_df = results_df.append(row, ignore_index = True)
        else:
            results_df.loc[results_df['nb_id'] == nb_id, 'errors'] = error

        print('wrote error for notebook ' + str(nb_id))

print(colored('successfully finished writing errors', 'green'))
results_df.to_csv('full_all_data.csv')
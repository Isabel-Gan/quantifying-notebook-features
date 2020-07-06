import pandas as pd
import csv

# notebook data
csv_directory = '../../test-dataset/notebooks_sample.csv'
notebooks_df = pd.read_csv(csv_directory)

# dataframes of the result data
third_run = pd.read_csv('third-run/github2017-third-run.csv')
sixth_run = pd.read_csv('sixth-run/github2017-sixth-run.csv')
eigth_run = pd.read_csv('eigth-run/github2017-eigth-run.csv')

# dataframe of most accurate error data
errors = pd.read_csv('sixth-run/github2017-sixth-errors.csv')

# fields associated with which sheet has the respective final data
field_files = {
    'longer_beginning' : eigth_run,
    'longer_ending' : eigth_run,
    'has_author' : sixth_run,
    'has_equation' : third_run,
    'jupyter_prop' : third_run,
    'output_cell_prop' : third_run,
    'markdown_prop' : third_run,
    'num_contrib' : third_run,
    'image_prop' : third_run,
    # 'e_keywords' : third_run,
    # 'p_keywords' : third_run,
    # 's_keywords' : third_run,
    'is_education' : sixth_run,
    'language' : sixth_run,
    'has_links' : sixth_run,
    'has_comments' : sixth_run,
    'md_frequency' : eigth_run,
    'has_title' : eigth_run,
    'num_commits' : eigth_run,
    'md_format' : eigth_run,
    'non_exec_prop' : eigth_run,
    'exec_inorder' : eigth_run,
    'exec_skips' : eigth_run,
    'has_error' : eigth_run,
    'speaking_language' : eigth_run
}

# template for a row written to the .csv file
row_write = {
    'nb_id' : None,
    'error' : None,
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
    'speaking_language' : None
}

# output path of gathered data
output_path = 'all_data.csv'

with open(output_path, 'w', newline='') as outcsv:

    writer = csv.DictWriter(outcsv, fieldnames = list(row_write.keys()))
    writer.writeheader()

    # iterate through all notebooks
    for row in notebooks_df.itertuples():

        # get the notebook id
        nb_id = row.nb_id
        row_write['nb_id'] = nb_id

        # check for an error in the notebook
        error_row = errors.loc[errors['nb_id'] == nb_id]
        error = None
        row_write['error'] = None
        if not error_row.empty:
            error = error_row['err_in'].item()
            row_write['error'] = error 
        
        # if there was an api, no_code, or nb_file error, then don't write field data
        if error not in ["api", "no_code", "nb_file"]:

            # write each of the features to the csv file
            for field in field_files:

                # get the dataframe associated with that field
                df = field_files[field]

                # get the row of the dataframe with the notebook id, if it exists
                df_row = df.loc[df['nb_id'] == nb_id]
                if not df_row.empty:
                    row_write[field] = df_row[field].item()

        # write the row to the csv and clear the row
        writer.writerow(row_write)  
        row_write = dict.fromkeys(row_write, None)

'''

data cleaning will be done later in a jupyter notebook:
- get rid of all the rows with api, no_code, nb_file errors
- filter down to english and python notebooks
- have to determine some value to put for the empty cells for each field

'''

import csv
import os
import re
import sys
import pandas as pd
from GitHubAPI_Crawler.github_api import GitHubAPI
from termcolor import colored
import api_cache

dbg_print = print

api = GitHubAPI()

# import scripts
import full_data_access as data
import markdown_analysis as md_analysis   
import notebook_analysis as nb_analysis   
import keyword_analysis as kw_analysis   
import repo_analysis
import code_analysis

# generates a certain number of segments
def get_segments(num_segments):
    
    # segment properties
    total_nbs = 143125
    segments = []
    segment_size = int(total_nbs / num_segments)

    # generate each segment
    prev_end = None
    for i in range(num_segments):

        if prev_end == None:
            segments.append((0, segment_size))
            prev_end = segment_size 
        elif i == num_segments - 1:
            segments.append((prev_end + 1, total_nbs - 1))
        else:
            new_end = (prev_end + 1) + segment_size
            segments.append((prev_end + 1, new_end))
            prev_end = new_end

    return segments

# get the number of segments we want
segments = get_segments(4)
segment_num = int(sys.argv[1])
cur_segment = segments[segment_num]

# dictionary object relating functions to their specific field in the csv
function_columns = {
    'longer_beginning' : md_analysis.longer_beginning,
    'longer_ending' : md_analysis.longer_ending,
    'has_author' : nb_analysis.has_author,
    'has_equation' : md_analysis.has_equations,
    'jupyter_prop' : repo_analysis.jupyter_prop,
    'output_cell_prop' : code_analysis.output_cell_prop,
    'markdown_prop' : md_analysis.markdown_prop,
    'num_contrib' : repo_analysis.num_contributors,
    'image_prop' : code_analysis.image_prop,
    # 'e_keywords' : kw_analysis.count_exploratory_keywords,
    # 'p_keywords' : kw_analysis.count_pipeline_keywords,
    # 's_keywords' : kw_analysis.count_sharing_keywords,
    'is_education' : nb_analysis.is_education,
    'language' : nb_analysis.get_language,
    'has_links' : md_analysis.has_links,
    'has_comments' : code_analysis.has_comments,
    'md_frequency' : md_analysis.frequency,
    'has_title' : nb_analysis.has_title,
    'num_commits' : repo_analysis.num_commits,
    'md_format' : md_analysis.md_formatting,
    'non_exec_prop' : code_analysis.non_executed_prop,
    'exec_inorder' : code_analysis.forwards_prop,
    'exec_skips' : code_analysis.ex_skip_average,
    'has_error' : code_analysis.has_error, 
    # 'comm_messages' : repo_analysis.get_commit_messages,
    'speaking_language' : nb_analysis.get_speaking_language,
    'has_export' : code_analysis.has_export,
    'num_functions' : code_analysis.num_functions,
    'has_test' : code_analysis.has_testing,
    'num_headers' : nb_analysis.num_headers,
    'has_param' : code_analysis.has_param,
    'has_reqtext' : repo_analysis.has_requirements,
    'num_stars' : repo_analysis.num_stars
}

# dictionary object with fields to hold rows to write
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
    'num_stars' : None
}

# dictionary object with fields to hold error rows to write
error_row = {
    'nb_id' : None,
    'repo_id' : None,
    'err_in' : None
}

# path to output csv
output_path = 'full-output/segments/second-run-segment' + str(segment_num) + '.csv'

# path to error csv
error_path = 'full-output/segments/second-errors-segment' + str(segment_num) + '.csv'

# dataset csv
notebooks_df = pd.read_pickle('full-dataset/notebooks.pkl')

# number of notebooks to run for, if applicable
limit = 1

# instantiate the api cache
api_cache.init_cache()

# writes to the csv
with open(output_path, 'w', newline='') as outcsv, open(error_path, 'w', newline='') as errorcsv:

    # writes column headers
    writer = csv.DictWriter(outcsv, fieldnames = row.keys())
    writer.writeheader()

    error_writer = csv.DictWriter(errorcsv, fieldnames = error_row.keys())
    error_writer.writeheader()

    # iterates over the notebooks in the notebook.csv
    success_counter = 0
    counter = 0
    err = False 
    for nb_id in range(cur_segment[0], cur_segment[1] + 1):

        # get notebook row
        notebook = notebooks_df.loc[notebooks_df['nb_id'] == nb_id].squeeze()

        # notebook identifier to print
        identifier = str((notebook['filepath'], str(notebook['nb_id'])))

        # get notebook and repository id
        nb_id = notebook['nb_id']
        repo_id = notebook['repo_id']

        # try generating the row of data
        row['nb_id'] = error_row['nb_id'] = nb_id
        row['repo_id'] = error_row['repo_id'] = repo_id 

        # check if notebook has been filtered
        if notebook['filtered']:
            error_row['err_in'] = 'filtered out'
            error_writer.writerow(error_row)
            continue 

        # check code cells may error if notebook file is empty
        try:
            # skip if there aren;t any code cells
            if len(data.get_code_cells(nb_id)) == 0:
                print(colored(identifier + ' has no code', 'yellow'))
                error_row['err_in'] = 'no code'
                error_writer.writerow(error_row)
                continue 
        except:
            print(colored("nb file error in " + identifier, 'red'))
            error_row['err_in'] = 'nb file' 
            error_writer.writerow(error_row)
            continue 
    
        # check the api response
        repo_link = data.get_repo_metadata(nb_id)['url']
        dbg_print('requesting for test')
        response = api.request(data.strip_url(repo_link))
        if 'id' not in response.keys():
            print(colored("api error in " + identifier, 'red'))
            error_row['err_in'] = 'api'
            error_writer.writerow(error_row)
            continue 

        # run the notebook through all functions
        for field in function_columns:
            function = function_columns[field]

            # try writing to the row, write none and to the error csv if there's an error
            try:
                row[field] = function(nb_id)
            except:
                print(colored('error in ' + identifier + ' in ' + field, 'red'))
                row[field] = None
                err = True 

                # write to the error csv
                error_row['err_in'] = field
                error_writer.writerow(error_row)
            
        # write the row
        writer.writerow(row)
        print("wrote " + identifier)

        # increment success counter if no error, reset error indicator
        if not err:
            success_counter += 1
        err = False 

        # increment regular counter
        counter += 1
        if counter == limit:
            break 

    print(colored("finished! successfully ran " + str(success_counter) + \
                    ' notebooks for segment ' + str(segment_num), 'green'))
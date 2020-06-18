import csv
import os
import re
from GitHubAPI_Crawler.github_api import GitHubAPI

# import scripts
import data_access as data
import markdown_analysis as md_analysis   
import notebook_analysis as nb_analysis   
import keyword_analysis as kw_analysis   
import repo_analysis

# dictionary object relating functions to their specific field in the csv
function_columns = {
    'longer_beginning' : md_analysis.longer_beginning,
    'longer_ending' : md_analysis.longer_ending,
    'has_author' : nb_analysis.has_author,
    'has_equation' : md_analysis.has_equations,
    'jupyter_prop' : repo_analysis.jupyter_prop,
    'output_cell_prop' : nb_analysis.output_cell_prop,
    'markdown_prop' : md_analysis.markdown_prop,
    'num_contrib' : repo_analysis.num_contributors,
    'image_prop' : nb_analysis.image_prop,
    'e_keywords' : kw_analysis.count_exploratory_keywords,
    'p_keywords' : kw_analysis.count_pipeline_keywords,
    's_keywords' : kw_analysis.count_sharing_keywords,
    'is_education' : nb_analysis.is_education,
    'language' : nb_analysis.get_language
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
    'e_keywords' : None,
    'p_keywords' : None,
    's_keywords' : None,
    'is_education' : None,
    'language' : None
}

# dictionary object with fields to hold error rows to write
error_row = {
    'nb_id' : None,
    'repo_id' : None,
    'err_in' : None
}

# path to output csv
output_path = 'output/test.csv'

# path to error csv
error_path = 'output/test-errors.csv'

# path to dataset
dataset_path = 'test-dataset/'

# directory of notebook files
directory = os.fsencode(dataset_path + 'notebooks')

# api crawler
api = GitHubAPI()

# writes to the csv
with open(output_path, 'w', newline='') as outcsv, open(error_path, 'w', newline='') as errorcsv:

    # writes column headers
    writer = csv.DictWriter(outcsv, fieldnames = row.keys())
    writer.writeheader()

    error_writer = csv.DictWriter(errorcsv, fieldnames = error_row.keys())
    error_writer.writeheader()

    # iterates over the files in the dataset directory
    counter = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # get notebook and repository id
        nb_id = int(re.findall("\d+", filename)[0])
        repo_id = data.get_repo_id(nb_id)

        # try generating the row of data
        row['nb_id'] = error_row['nb_id'] = nb_id
        row['repo_id'] = error_row['repo_id'] = repo_id

        # skip if there aren't any code cells
        if len(data.get_code_cells(nb_id)) == 0:
            error_row['err_in'] = 'no_code'
            error_writer.writerow(error_row)
            continue

        # check the api response
        repo_link = data.get_repo_metadata(nb_id)['url']
        response = api.request(data.strip_url(repo_link))
        if 'id' not in response.keys():
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
                print("error in " + filename)
                row[field] = None

                # write to the error csv
                error_row['err_in'] = field
                error_writer.writerow(error_row)

        # write the row
        writer.writerow(row)
        print("wrote " + filename)
        counter += 1
    
    print("finished! successfully ran " + str(counter) + " notebooks")





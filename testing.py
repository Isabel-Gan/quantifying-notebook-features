import pandas as pd

# import all the scripts
import data_access as data   
import markdown_analysis as md_analysis
import notebook_analysis as nb_analysis 
import repo_analysis 
import keyword_analysis as kw_analysis
import code_analysis 

''' testing a single function at a time - print out results '''

# ids of notebooks to test
nb_ids = [602217, 1051197, 466289, 958849, 972721, 1019165,
            972366, 219322, 464706, 333748, 1047986, 1124656,
            492523, 1081631, 681455, 531968, 578489, 165313,
            439119, 884271, 390160, 457759, 608191, 514544,
            672138, 323880, 987671, 329885, 718440, 116896,
            625482, 295335, 502567, 912876, 672725, 654583]

# prints out the results of running a function on all notebooks
def test_func(func):
    print("testing " + str(func))
    for nb_id in nb_ids:
        try:
            print(str(nb_id) + " : " + str(func(nb_id)))
        except:
            print("error in notebook " + str(nb_id) + " repository " + str(data.get_repo_id(nb_id)))
            raise

# PUT TESTS HERE
test_func(code_analysis.has_error)

''' testing all functions - print out results '''

# functions to give to test_all
feature_tests = [md_analysis.longer_beginning, md_analysis.longer_ending, nb_analysis.has_author, 
                md_analysis.has_equations, repo_analysis.jupyter_prop, code_analysis.output_cell_prop,
                md_analysis.markdown_prop, repo_analysis.num_contributors, code_analysis.image_prop,
                kw_analysis.count_exploratory_keywords, kw_analysis.count_pipeline_keywords, 
                kw_analysis.count_sharing_keywords, nb_analysis.is_education, nb_analysis.get_language,
                code_analysis.has_comments]

# tests all functions in list above on all notebooks in the test dataset
def test_all():
    for feature in feature_tests:
        test_func(feature)

# test_all()

''' testing a single function at a time - comparing results for correctness '''

# dictionary object relating functions to their specific field in the csv
function_columns = {
    'longer_beginning' : md_analysis.longer_beginning,
    'longer_ending' : md_analysis.longer_ending,
    'has_author' : nb_analysis.has_author,
    'has_equation' : md_analysis.has_equations
}

# load in the results csv file
df_results = pd.read_csv('test-dataset/testing_results.csv')

def check(field):
    print("testing " + str(field))

    # for each notebook in the testing dataset
    for nb_id in nb_ids:
        # check if the function result is equal to what's in the table
        func_res = function_columns[field](nb_id)
        true_res = int(df_results.loc[df_results['nb_id'] == nb_id][field])

        if func_res != true_res:

            # check for none result
            if not (func_res == None and true_res == -1):
                print("notebook " + str(nb_id) + ":")
                print("function returns " + str(func_res))
                print("true result is " + str(true_res))
                print("\n")

# PUT TESTS HERE

''' testing all functions - comparing results for correctness '''

# tests all objects in the dictionary against their corresponding functions
def check_results():

    # for each field to test against
    for field in function_columns:
        check(field)
        print("\n")

# check_results()


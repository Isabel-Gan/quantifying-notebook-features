# import all the scripts
import data_access as data   
import markdown_analysis as md_analysis
import notebook_analysis as nb_analysis 
import repo_analysis 

# ids of notebooks to test
nb_ids = [165313, 219322, 333748, 439119, 464706, 
            466289, 492523, 531968, 578489, 602217,
            681455, 884271, 958849, 972366, 972721,
            1019165, 1047986, 1051197, 1081631, 1124656]

# prints out the results of running a function on all notebooks
def test_func(func):
    for nb_id in nb_ids:
        try:
            print(str(nb_id) + " : " + str(func(nb_id)))
        except:
            print("error in notebook " + str(nb_id) + " repository " + str(data.get_repo_id(nb_id)))
            raise

# PUT TESTS HERE

# functions to give to test_all
feature_tests = [md_analysis.longer_beginning, md_analysis.longer_ending, nb_analysis.has_author, 
                md_analysis.has_equations, repo_analysis.jupyter_prop, nb_analysis.output_cell_prop,
                md_analysis.markdown_prop, repo_analysis.num_contributors]

# tests all functions in list above on all notebooks in the test dataset
def test_all():
    for feature in feature_tests:
        print("testing " + str(feature))
        test_func(feature)

test_all()

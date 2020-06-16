import data_access as data    

# keywords associated with sharing notebooks
sharing_keywords = ["blog", "examples", "presentation", "results"]

# keywords associated with pipeline/production notebooks
pipeline_keywords = ["preprocessing", "snippets", "fragments", "customize", 
                        "tools", "development", "formatter"]

# keywords associated with exploratory notebooks
exploratory_keywords = ["attempt", "experiment", "fun", "exploring", 
                        "comparison", "playground"]

''' feature - sharing keywords '''

# counts the number of keyword hits in the notebook markdown cells
def keyword_search(keyword_set, nb_id):

    # get the markdown cells
    md_cells = data.get_md_cells(nb_id)

    # go through the markdown cells and search for the keywords
    num_hits = 0
    for cell in md_cells:
        for line in cell['source']:

            # make sure to search for each keyword
            for keyword in keyword_set:
                if keyword in line:
                    num_hits += 1
    
    return num_hits

# counts the number of sharing keywords used in the notebook markdown cells)
def count_sharing_keywords(nb_id):
    return keyword_search(sharing_keywords, nb_id)

# counts the number of pipeline/production keywords used in the notebook markdown cells)
def count_pipeline_keywords(nb_id):
    return keyword_search(pipeline_keywords, nb_id)

# counts the number of exploratory keywords used in the notebook markdown cells)
def count_exploratory_keywords(nb_id):
    return keyword_search(exploratory_keywords, nb_id)

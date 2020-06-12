import data_access as data   

# calculates the proportion of code in the repo written in jupyter
def jupyter_prop(nb_id):

    # get the language data
    languages_data = data.get_languages(nb_id)
    keys = languages_data.keys()

    # check if language data is recorded and jupyter notebook is part of it
    if 'Jupyter Notebook' in keys:

        # calculate the sum of bytes of code in the repo
        bytes_sum = 0
        for key in keys:
            bytes_sum += languages_data[key]
        
        # calculate the proportion of code in jupyter
        bytes_jupyter = languages_data['Jupyter Notebook']
        return float(bytes_jupyter) / float(bytes_sum)

    # if language data not recorded/jupyter notebook not in data
    else:
        return -1

# tests - delete later
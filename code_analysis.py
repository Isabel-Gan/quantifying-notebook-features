import data_access as data   

''' feature - comments in code '''
def has_comments(nb_id):

    # get comments
    comments = data.get_comments(nb_id)

    # check if any exist
    if comments != None:
        return len(comments) != 0
    else:
        return None
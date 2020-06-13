import data_access as data  

''' feature - author '''

# gets the full name of author of the repo of the notebook
def get_author(nb_id):
    author_url_data = data.get_owner_url(nb_id)
    return author_url_data['name']

# gets the username of author of the repo of the notebook
def get_username(nb_id):
    author_url_data = data.get_owner_url(nb_id)
    return author_url_data['login']

# searches all cells for instances of an author username or name
def has_author(nb_id):

    # get all the cells and author names
    cells = data.get_cells(nb_id)
    author_name = get_author(nb_id)
    author_login = get_username(nb_id)

    # check each cell for an author
    for cell in cells:

        # check for which field holds the content
        keys = cell.keys()
        if 'source' in keys:
            lines = cell['source']
        else:
            lines = cell['input']

        # scan all the lines in the cell
        for line in lines:
            if (author_name in line) | (author_login in line):
                return True

    return False
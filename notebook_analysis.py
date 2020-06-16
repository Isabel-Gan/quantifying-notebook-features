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

            if author_name != None:
                if author_name in line:
                    return True

            if author_login != None:
                if author_login in line:
                    return True

    return False

''' feature - proportion of code cells with output '''

# counts the number of code cells with output
def output_cells(nb_id):

    # get code cells
    code_cells = data.get_code_cells(nb_id)

    # filter and get the length of the filtered list
    output_cells = list(filter(lambda cell : len(cell['outputs']) > 0, code_cells))
    return len(output_cells)

# calculates the proportion of code cells with output
def output_cell_prop(nb_id):

    num_code_cells = len(data.get_code_cells(nb_id))
    num_output_cells = output_cells(nb_id)

    return float(num_output_cells) / float(num_code_cells)

''' feature - images (tables/graphs) as output '''

# counts the number of output cells that contain an image (including graphs)
def count_images(nb_id):

    # get code cells
    output_cells = data.get_code_cells(nb_id)

    # for each code cell, checks the outputs if they have an image
    image_outputs = 0
    for cell in output_cells:
        for output in cell['outputs']:

            # field associated with displaying an image
            if output['output_type'] == "display_data":

                # double-check that an image is actually being displayed
                keys = output.keys()
                if "png" in keys:
                    image_outputs += 1
                    break
                elif "data" in keys:
                    if "image/png" in output['data'].keys():
                        image_outputs += 1
                        break
    
    return image_outputs

# calculates the proportion of output cells that contain an image or table
def image_prop(nb_id):

    num_image_outputs = count_images(nb_id)
    num_table_outputs = 0 # REPLACE LATER
    num_outputs = output_cells(nb_id)

    # if there are no output cells, immediately return
    if num_outputs == 0:
        return -1

    return float(num_image_outputs + num_table_outputs) / float(num_outputs)


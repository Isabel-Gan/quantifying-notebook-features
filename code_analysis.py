import data_access as data   

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

# counts the number of output cells that contain an image (including graphs) or table
def count_images(nb_id):

    # get code cells
    output_cells = data.get_code_cells(nb_id)

    # for each code cell, checks the outputs if they have an image
    image_outputs = 0
    has_image = False
    for cell in output_cells:
        for output in cell['outputs']:

            # field associated with displaying an image
            if output['output_type'] == "display_data":

                # double-check that an image is actually being displayed
                keys = output.keys()
                if "png" in keys:
                    image_outputs += 1
                    has_image = True

                elif "data" in keys:
                    if "image/png" in output['data'].keys():
                        image_outputs += 1
                        has_image =  True

            # fields associated with displaying a table
            elif 'data' in output.keys() and 'text/html' in output['data'].keys():

                # double-check that a table is actually being displayed
                for line in output['data']['text/html']:
                    if "</table>" in line:
                        image_outputs += 1
                        has_image = True
                        break
            
            # if image already found, stop checking this output cell
            if has_image:
                has_image = False
                break
    
    return image_outputs

# calculates the proportion of output cells that contain an image or table
def image_prop(nb_id):

    num_image_outputs = count_images(nb_id)
    num_outputs = output_cells(nb_id)

    # if there are no output cells, immediately return
    if num_outputs == 0:
        return None

    return float(num_image_outputs) / float(num_outputs)

''' feature - comments in code '''

def has_comments(nb_id):

    # get comments
    comments = data.get_comments(nb_id)

    # check if any exist
    if comments != None:
        return len(comments) != 0
    else:
        return None
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

# checks if comments exist in any code cells in a notebook
def has_comments(nb_id):

    # get comments
    comments = data.get_comments(nb_id)

    # check if any exist
    if comments != None:
        return len(comments) != 0
    else:
        return None

''' feature - proportion of non-executed code cells '''

# gets the execution count of a code cell in a notebook
def get_exec(cell):

    # check which key is holding execution count info
    keys = cell.keys()
    field = ""
    if 'execution_count' in keys:
        field = 'execution_count'
    elif 'prompt_number' in keys:
        field = 'prompt_number'
    else:
        # if this information isn't recorded, assume the cell hasn't been executed
        return 0
    
    # extract execution count info
    try:
        return int(cell[field])
    except:
        return 0

# counts the number of non-executed, non-empty code cells in a notebook
def count_non_exec(nb_id):
    
    # get code cells
    code_cells = data.get_code_cells(nb_id)

    # filter down to those that have a non-empty source 
    def condition(cell):
        keys = cell.keys()
        field = ""
        if 'input' in keys:
            field = 'input'
        elif 'source' in keys:
            field = 'source'

        return len(cell[field]) > 0

    non_empty_code_cells = list(filter(condition, code_cells))

    # filter down to those that have 0 execution count
    non_executed_code_cells = list(filter(lambda cell : get_exec(cell) == 0, non_empty_code_cells))

    # return the length of the filtered list
    return len(non_executed_code_cells)

# calculates the proportion of code cells in a notebook that are non-executed
def non_executed_prop(nb_id):

    # get number of code cells and non-executed code cells
    num_code_cells = len(data.get_code_cells(nb_id))
    num_non_executed = count_non_exec(nb_id)

    # calculate proportion
    return float(num_non_executed) / float(num_code_cells)

''' feature - errors '''

# returns true if there is an executed code cell with an error output
def has_error(nb_id):

    # get code cells
    code_cells = data.get_code_cells(nb_id)

    # filter down to those that have been executed
    ex_code_cells = list(filter(lambda cell : get_exec(cell) > 0, code_cells))

    # iterate through and check outputs
    for cell in ex_code_cells:
        
        # check outputs
        if 'outputs' in cell.keys():
            for output in cell['outputs']:
                if output['output_type'] == "error" or output['output_type'] == "pyerr":
                    return True

    return False

''' feature - execution order - top-down '''

# counts the number of times execution order goes backwards
def count_backwards(nb_id):

    # get code cells that have been executed
    code_cells = data.get_code_cells(nb_id)
    ex_code_cells = list(filter(lambda cell : get_exec(cell) > 0, code_cells))  

    # iterate through and count the number of times execution order goes backwards
    backsteps = 0
    for (i, cell) in enumerate(ex_code_cells):

        # if not on the last cell, check the next cell
        if i != len(ex_code_cells) - 1:

            # count if execution order goes backwards
            if get_exec(cell) < get_exec(ex_code_cells[i + 1]):
                backsteps += 1
    
    return backsteps

# calculates the proportion of executed code cell borders that have a backwards execution order
def backwards_prop(nb_id):

    # get code cells that have been executed
    code_cells = data.get_code_cells(nb_id)
    ex_code_cells = list(filter(lambda cell : get_exec(cell) > 0, code_cells))

    # if no code cells have been executed, return immediately
    if len(ex_code_cells) == 0:
        return None

    # get number of backwards steps and number of steps
    back_steps = count_backwards(nb_id)
    steps = len(ex_code_cells) - 1

    return float(back_steps) / float(steps)

''' feature - execution order - skips '''

# calculates the average size of an execution order skip in a notebook
def ex_skip_average(nb_id):

    # get code cells that have been executed
    code_cells = data.get_code_cells(nb_id)
    ex_code_cells = list(filter(lambda cell : get_exec(cell) > 0, code_cells))

    # if no code cells have been executed, return immediately
    if len(ex_code_cells) == 0:
        return None
    
    # get sum of skips in execution order
    sum_skips = 0
    for (i, cell) in enumerate(ex_code_cells):
        
        # if not on the last cell get the size of the skip
        if i != len(ex_code_cells) - 1:
            sum_skips += abs(get_exec(ex_code_cells[i + 1]) - get_exec(cell))
    
    # calculate the average size of a skip
    return float(sum_skips) / float(len(ex_code_cells) - 1)
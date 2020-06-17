import data_access as data
import re

''' feature - amount of markdown cells in the notebook '''

# calculates the proportion of markdown cells in a notebook
def markdown_prop(nb_id):
    
    num_cells = len(data.get_cells(nb_id))
    num_md = len(data.get_md_cells(nb_id))

    return (float(num_md) / float(num_cells))

''' feature - longer markdown cells in the beginning/end of the notebook '''

# minimum margin to be greater than the avg. markdown cell
min_margin = 70

def get_char_length(md_cell):

    # sum the lengths of all lines of source in the cell
    length = 0
    for line in md_cell['source']:
        length += len(line)
    
    return length

# calculates the average length of markdown cells in a notebook (by characer)
def markdown_average(nb_id):

    # get markdown cells
    md_cells = data.get_md_cells(nb_id)
    num_md = len(md_cells)

    # calculate the length sum of markdown cells
    len_sum = 0
    for md_cell in md_cells:
        len_sum += get_char_length(md_cell)

    # calculate and return the average length
    if num_md == 0:
        return 0
    else:
        return float(len_sum) / float(num_md)

# returns true if one of the first five cells is a longer markdown cell
def longer_beginning(nb_id):

    # get the average length of a markdown cell in the notebook
    md_average = markdown_average(nb_id)

    # if there are no markdown cells, immediately return
    if md_average == 0:
        return None

    # check the first five notebook cells
    first_five_cells = data.get_cells(nb_id)[:4]
    for cell in first_five_cells:
        if cell['cell_type'] == "markdown":
            if get_char_length(cell) >= (md_average + min_margin):
                return True

    return False

# returns true if one of the last five cells is a longer markdown cell
def longer_ending(nb_id):

    # get the average length of a markdown cell in the notebook
    md_average = markdown_average(nb_id)

    # if there are no markdown cells, immediately return
    if md_average == 0:
        return None

    # check the last five markdown cells
    last_five_cells = data.get_cells(nb_id)[-5:]
    for cell in last_five_cells:
        if cell['cell_type'] == "markdown":
            if get_char_length(cell) >= (md_average + min_margin):
                return True
    
    return False

''' feature - equations '''

def has_equations(nb_id):

    # pattern to look for equation (math mode)
    pattern = "\$([\S\s]+)\$"

    # get all the markdown cells
    md_cells = data.get_md_cells(nb_id)

    # if there are no markdown cells, return immediately
    if len(md_cells) == 0:
        return None

    # search the markdown cells for equations
    for cell in md_cells:
        for line in cell['source']:
            if re.search(pattern, line):
                return True

    return False

# tests - delete later

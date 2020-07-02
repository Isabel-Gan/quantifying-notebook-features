import data_access as data
import notebook_analysis as nb_analysis 

import html2text 
import re
import regex
import mistune

''' feature - amount of markdown cells in the notebook '''

# calculates the proportion of markdown cells in a notebook
def markdown_prop(nb_id):
    
    num_cells = len(data.get_cells(nb_id))
    num_md = len(data.get_md_cells(nb_id))

    return (float(num_md) / float(num_cells))

''' feature - longer markdown cells in the beginning/end of the notebook '''

# minimum margin to be greater than the avg. markdown cell
min_margin = 10

# given a group of markdown cells, takes their length to be the number of words in each
def get_length(md_group):

    # iterate through each cell in the group
    length = 0
    for md_cell in md_group:

        # check if the markdown cell actually has a source
        if 'source' not in md_cell.keys():
            return 0

        # sum the lengths of all lines of source in the cell
        for line in md_cell['source']:

            # filter out the equations, count them as one word
            equation = re.search(regex.equation, line)
            while equation != None:
                length += 1
                line = line.replace(equation.group(0), "")
                equation = re.search(regex.equation, line)

            # get the number of words in the remaining line
            text = html2text.html2text(line).strip()
            length += len(text.split())
    
    return length

# calculates the average length of markdown cell groups in a notebook (by words)
def markdown_average(nb_id):

    # get markdown cell groups
    md_groups = data.get_md_groups(nb_id)
    num_groups = len(md_groups)

    # calculate the length sum of markdown cells
    len_sum = 0
    for md_group in md_groups:
        len_sum += get_length(md_group)

    # calculate and return the average length
    if num_groups == 0:
        return 0
    else:
        return float(len_sum) / float(num_groups)

# given groups of md cells and a md cell, returns the group that cell is part of
def get_md_group(md_groups, md_cell):

    # iterate through the groups and find the right one
    for md_group in md_groups:
        if md_cell in md_group:
            return md_group 

    # not found
    return None

# returns true if one of the first five cells is a longer markdown cell
def longer_beginning(nb_id):

    # get the average length of a markdown group in the notebook
    md_groups = data.get_md_groups(nb_id)
    md_average = markdown_average(nb_id)

    # if there are < 10 cells, immediately return
    if nb_analysis.is_small_nb(nb_id):
        return None

    # if there are no markdown cells, immediately return
    if md_average == 0:
        return None

    # check the first five notebook cells
    first_five_cells = data.get_cells(nb_id)[:4]
    for cell in first_five_cells:
        if cell['cell_type'] == "markdown":

            # get the md group the cell is part of
            md_group = get_md_group(md_groups, cell)
            if get_length(md_group) >= (md_average + min_margin):
                return True

    return False

# returns true if one of the last five cells is a longer markdown cell
def longer_ending(nb_id):

    # get the average length of a markdown group in the notebook
    md_groups = data.get_md_groups(nb_id)
    md_average = markdown_average(nb_id)

    # if there are < 10 cells, immediately return
    if nb_analysis.is_small_nb(nb_id):
        return None

    # if there are no markdown cells, immediately return
    if md_average == 0:
        return None

    # check the last five markdown cells
    last_five_cells = data.get_cells(nb_id)[-5:]
    for cell in last_five_cells:
        if cell['cell_type'] == "markdown":

            # get the md group the cell is part of
            md_group = get_md_group(md_groups, cell)
            if get_length(md_group) >= (md_average + min_margin):
                return True
    
    return False

''' feature - equations '''

def has_equations(nb_id):

    # get all the markdown cells
    md_cells = data.get_md_cells(nb_id)

    # if there are no markdown cells, return immediately
    if len(md_cells) == 0:
        return None

    # search the markdown cells for equations
    for cell in md_cells:

        # check if markdown cell has source field
        if 'source' not in cell.keys():
            continue

        for line in cell['source']:
            if re.search(regex.equation, line):
                return True

    return False

''' feature - links '''

def has_links(nb_id):

    # get all the markdown cells
    md_cells = data.get_md_cells(nb_id)

    # if there are no markdown cells, return immediately
    if len(md_cells) == 0:
        return None

    # search the markdown cells for links
    for cell in md_cells:

        # check if markdown cell has source field
        if 'source' not in cell.keys():
            continue

        for line in cell['source']:
            if re.search(regex.link, line) and not re.search(regex.img_src, line):
                return True

    return False

''' feature - frequency of markdown cells '''

# counts the number of "switches" between code and markdown in a notebook
def count_switches(nb_id):

    # get the cells
    cells = data.get_cells(nb_id)

    # iterate through and count switches
    switches = 0
    for (i, cell) in enumerate(cells):

        # check the next cell if we are not on the last cell
        if i != len(cells) - 1:

            # code -> markdown
            if cell['cell_type'] == "code" and cells[i + 1]['cell_type'] == "markdown":
                switches += 1

            # markdown -> code
            if cell['cell_type'] == "markdown" and cells[i + 1]['cell_type'] == "code":
                switches += 1
    
    return switches

# calculates the proportion of cell switches that are between code and markdown 
def frequency(nb_id):

    # check if markdown cells exist
    if len(data.get_md_cells(nb_id)) == 0:
        return None

    # get the number of code <-> markdown switches and the number of total switches
    cm_switches = count_switches(nb_id)
    total_switches = len(data.get_cells(nb_id)) - 1

    # calculate proportion
    return float(cm_switches) / float(total_switches)

''' feature - markdown formatting '''

# "extra" formatting features 
extra_formatting = ["image", "list", "block_quote"]

# checks a markdown parsed token for whether it (or its children) has extra formatting or not
def is_extra_formatting(token):
    
    # check the type of the token itself
    for e_format in extra_formatting:
        if e_format == token['type']:
            return True
    
    # check the children 
    if 'children' in token.keys():
        for child in token['children']:
            if isinstance(child, dict) and is_extra_formatting(child):
                return True

    return False

# takes in a markdown cell, determines whether it has "extra" formatting or not
def has_extra_formatting(cell):

    if 'source' not in cell.keys():
        return False

    # gather the entire markdown cell source as one string
    markdown_source = "".join(cell['source'])

    # pass to the markdown parser to generate tokens
    markdown = mistune.create_markdown(renderer=mistune.AstRenderer())
    markdown_tokens = markdown(markdown_source)
   
    # iterate through tokens to check for extra formatting
    for token in markdown_tokens:
       if is_extra_formatting(token):
           return True

    return False
    
# determines whether the markdown cells in a notebook have extra formatting
def md_formatting(nb_id):

    # gather markdown cells
    md_cells = data.get_md_cells(nb_id)

    # if there are no markdown cells, return immediately
    if len(md_cells) == 0:
        return None

    # iterate through and check whether they have special formatting
    for cell in md_cells:
        if has_extra_formatting(cell):
            return True 

    return False 
        
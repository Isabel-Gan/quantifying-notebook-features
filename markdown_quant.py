import data_access as data

def count_cells(nb_id):
    return len(data.get_cells(nb_id))

def count_markdown(nb_id):

    cells = data.get_cells(nb_id)
    md_count = 0

    # iterate through and count the markdown cells
    for cell in cells:
        if cell['cell_type'] == "markdown":
            md_count += 1
    
    return md_count

def markdown_prop(nb_id):
    
    num_cells = count_cells(nb_id)
    num_md = count_markdown(nb_id)

    return (float(num_md) / float(num_cells))

# tests - delete later

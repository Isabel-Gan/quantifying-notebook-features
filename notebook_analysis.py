import data_access as data  
import re

''' feature - author '''

# gets the full name of author of the repo of the notebook
def get_author(nb_id):
    author_url_data = data.get_owner_url(nb_id)
    return author_url_data['name']

# gets the username of author of the repo of the notebook
def get_username(nb_id):
    author_url_data = data.get_owner_url(nb_id)
    return author_url_data['login']

# gathers the usernames and names of contributors to the repository
def get_contributors(nb_id):

    # get contributor data
    contributors_data = data.get_repo_field(nb_id, 'contributors_url')

    # get author data to prevent duplicates
    author_name = get_author(nb_id)
    author_user = get_username(nb_id)

    # for each contributor, get their login and name:
    names = []
    for contributor in contributors_data:
        contributor_data = data.get_url(contributor['url'])
        name = contributor_data['name']
        login = contributor_data['login']

        # check for existence and duplicates
        if name != None and name != author_name:
            names += [name]

        if login != None and login != author_user:
            names += [login]

    return names

# searches markdown cells and code comments for instances of an author username or name
def has_author(nb_id):

    # get all the markdown cells and author names
    md_cells = data.get_md_cells(nb_id)

    author_name = get_author(nb_id)
    author_login = get_username(nb_id)
    all_names = get_contributors(nb_id) + [author_name, author_login]

    # check each cell for an author
    for cell in md_cells:

        if 'source' in cell.keys():
            lines = cell['source']

            # scan all the lines in the cell
            for line in lines:
                # check all possible authors
                for name in all_names:
                    if name != None and name in line:
                        return True

    # gather comments
    comments = data.get_comments(nb_id)
    
    # search each comment for the author names
    for comment in comments:
        for name in all_names:
            if name != None and name in comment:
                return True

    # no instances of authors found
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

''' feature - language '''

# returns the language of the notebook as a string
def get_language(nb_id):

    # get the notebook file
    nb = data.get_nb(nb_id)

    # look for the language
    language = ""
    keys = nb.keys()
    
    # check if language is stored in the cells or notebook metadata
    if 'worksheets' in keys:

        # then language data is in each cell, get code cells and get the language from one of them
        code_cells = data.get_code_cells(nb_id)
        for cell in code_cells:
            if language != "":
                break
            else:
                language = cell['language']
    
    else:
        # then language data is in the metadata
        language = nb['metadata']['kernelspec']['language']
    
    return language
            

''' feature - educational notebook '''

# regex associated with education notebooks
education_patterns = ["project", "hint", "rubric", "answer", "question", "pass",
                        "lesson", "lecture", "homework", "slides", "final-project",
                        "course", "assignment", "quiz", "submission","hw", "exercise", 
                        "due", "bootcamp", "assessment", "final_project",
                        "week([_\- ]|\B)([0-9]+)", "day([_\- ]|\B)([0-9]+)"]

# searches markdown cells and notebook name/path for any patterns above
def is_education(nb_id):
    
    # get the markdown cells
    md_cells = data.get_md_cells(nb_id)

    # go through the markdown cells and search for the keywords
    for cell in md_cells:
        for line in cell['source']:

            # make sure to search for each keyword
            for pattern in education_patterns:
                if re.search(pattern, line.lower()):
                    return True

    # check the file path (including the file name) for the keywords as well
    path = data.get_path(nb_id)
    for pattern in education_patterns:
        if re.search(pattern, path.lower()):
            return True
    
    return False
 
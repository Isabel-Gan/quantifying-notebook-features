import full_data_access as data  
import re
import regex
from langdetect import detect
from iso639 import languages

''' helper function -  less than 10 cells '''

# returns true if the notebook has < 10 cells
def is_small_nb(nb_id):

    # get cells
    cells = data.get_cells(nb_id)

    # check number of cells
    return len(cells) < 10

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

        # don't request author
        if contributor['login'] != author_user:
            contributor_data = data.get_url(contributor['url'])
            name = contributor_data['name']
            login = contributor_data['login']

            # check for existence and duplicates
            if name != None:
                names += [name]

            if login != None:
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

                # filter out links before searching for author
                link = re.search(regex.link, line)
                while link != None:
                    line = line.replace(link.group(0), "")
                    link = re.search(regex.link, line)

                # check all possible authors
                for name in all_names:
                    if name != None and name in line:
                        return True

    # gather comments
    comments = data.get_comments(nb_id)
    
    if comments != None:
        # search each comment for the author names
        for comment in comments:
            for name in all_names:
                if name != None and name in comment:
                    return True

    # no instances of authors found
    return False

''' feature - language '''

# returns the language of the notebook as a string
def get_language(nb_id):

    # get the notebook file
    nb = data.get_nb(nb_id)

    # look for the language
    language = None
    keys = nb.keys()
    
    # check if language is stored in the cells or notebook metadata
    if 'worksheets' in keys:

        # then language data is in each cell, get code cells and get the language from one of them
        code_cells = data.get_code_cells(nb_id)
        for cell in code_cells:
            if language != None:
                break
            else:
                language = cell['language']
  
    elif 'kernelspec' in nb['metadata'].keys():

        # then language data is in the metadata
        kernelspec = nb['metadata']['kernelspec']
        keys = kernelspec.keys()

        if 'language' in keys:
            language = kernelspec['language']
        elif 'name' in keys:
            language = kernelspec['name']
        else:
            language = None
    
    else:

        # language data not recorded
        language = None
    
    return language
            
''' feature - educational notebook '''

# searches markdown cells and notebook name/path for any patterns above
def is_education(nb_id):
    
    # get the markdown cells
    md_cells = data.get_md_cells(nb_id)

    # go through the markdown cells and search for the keywords
    for cell in md_cells:
        if 'source' in cell.keys():
            for line in cell['source']:
                # make sure to search for each keyword
                for pattern in regex.education:
                    if re.search(pattern, line.lower()):
                        return True

    # check the file path (including the file name) for the keywords as well
    path = data.get_path(nb_id)
    for pattern in regex.education:
        if re.search(pattern, path.lower()):
            return True
    
    return False
 
''' feature - notebook title '''

# determines whether the notebook has a title (a heading markdown at the beginning)
def has_title(nb_id):

    # get the cells
    cells = data.get_cells(nb_id)

    # get the first cell (should be markdown)
    for cell in cells:
        
        keys = cell.keys()

        # if the first thing is a code cell, return immediately
        if cell['cell_type'] == "code":
            return False

        # if in a markdown cell, check if non-empty, keep looking if empty
        if cell['cell_type'] == "markdown":

            # check for non-empty
            if 'source' in keys and len(cell['source']) > 0:
                # check for header
                return bool(re.match(regex.md_header, cell['source'][0]))
                
    return False

''' feature - language (non-programming) '''

# detects the language of some markdown cells
def speaking_language(cells):

    # gather the sources of the markdown cells together
    all_source = ""
    for cell in cells:
        
        if 'source' not in cell.keys():
            continue 
        
        lines = cell['source']
        lines_stripped = list(map(lambda line : line.strip(), lines))

        # after stripping each line, filter out the equations (math mode) and links from each line
        def filter_line(line):

            # filter out equations
            equation = re.search(regex.equation, line)
            while equation != None:
                line = line.replace(equation.group(0), "")
                equation = re.search(regex.equation, line)

            # filter out links
            link = re.search(regex.link, line)
            while link != None:
                line = line.replace(link.group(0), "")
                link = re.search(regex.link, line)

            return line

        lines_filtered = list(map(filter_line, lines_stripped))

        # gather the lines together
        source = " ".join(lines_filtered)

        # add the source of this markdown cell to the entire source
        all_source += " " + source
    
    # detect the language of the gathered source
    try:
        return languages.get(alpha2=detect(all_source)).name
    except:
        return None

# detects the speaking language of a notebook based on its markdown cells 
def get_speaking_language(nb_id):

    # gather the markdown cells
    md_cells = data.get_md_cells(nb_id)

    # if there are no markdown cells, return immediately
    if len(md_cells) == 0:
        return None 

    # get the language of the markdown cells
    return speaking_language(md_cells)

''' feature - notebook structure '''

# returns the number of markdown headers within a single cell
def count_headers(cell):

    num_headers = 0

    # check the cell source
    if 'source' in cell.keys():
        for line in cell['source']:
            if re.match(regex.md_header, line.strip()):
                num_headers += 1

    # return the total 
    return num_headers

# returns the number of markdown headers in a notebook
def num_headers(nb_id):

    # get the markdown cells
    md_cells = data.get_md_cells(nb_id)

    # count the number of headers across the cells
    num_headers = 0
    for cell in md_cells:
        num_headers += count_headers(cell)

    # return the total
    return num_headers


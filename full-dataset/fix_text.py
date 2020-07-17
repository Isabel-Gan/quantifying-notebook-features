import re

contents = 'hi :)'

# read the contents of the text file
with open('errors_segment3.txt', 'r') as file:
    contents = file.readline()

full_contents = []
    
# determine if we need to split the contents further
while sum(contents.count(x) for x in ['notebook', 'could not clone']) > 0:

    split_contents = re.search('could not clone (.*?), timed out', contents)
    if split_contents != None:
        contents = contents.replace(split_contents.group(0), '')
        full_contents.append(split_contents.group(0))

    split_contents = re.search('notebook ([0-9]+)', contents)
    if split_contents != None:
        contents = contents.replace(split_contents.group(0), '')
        full_contents.append(split_contents.group(0))

final_contents = '\n'.join(full_contents)

# write to the file 
with open('errors_segment3.txt', 'w') as file:
    file.write(final_contents)
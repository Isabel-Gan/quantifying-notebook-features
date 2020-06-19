# Interpreting the `err_in` column of `errors.csv`

`has_author`: an error when trying to obtain the names/usernames of authors or contributors, most likely means that an author or
contributor has changed their username so the url under the `repository_metadata` is no longer valid

`no_code`: the notebook file contained only markdown cells, so we filter this out

`nb_file`: notebook file is malformed (notebook files are read in as .json, but the file returns a 404 Not Found when loaded in)

`api`: the api was non-responsive, usually meaning that the repository/notebook link is no longer valid

`language`: language data not recorded in the notebook file'

for those notebooks that look like had a chain of errors, those were small bugs in my scripts, and will be/are already fixed

# quantifying-notebook-features

A collection of Python scripts to quantify and detect features of Jupyter notebooks. 

Modules/projects and datasets imported:

- [API Crawler](https://github.com/shuiblue/GitHubAPI-Crawler)

- [Markdown Parser](https://mistune.readthedocs.io/en/latest/index.html)

- [Python Comment Parser](https://pypi.org/project/comment-parser/)

- [HTML to Text Converter](https://pypi.org/project/html2text/)

- [Language Detector](https://pypi.org/project/langdetect/) and [ISO 639 Code Translator](https://pypi.org/project/iso-639/)

- [LRU Cache](https://pypi.org/project/pylru/) for API cache

- [Colored Terminal Output](https://pypi.org/project/termcolor2/)

- Testing dataset is a small subset from https://library.ucsd.edu/dc/object/bb2733859v

Created and used for Summer 2020 research on improving computational notebooks under Christian Kaestner and Shurui Zhou  at CMU ISR.

## file information

`api_cache.py`: uses an LRU cache implementation to handle operations on a cache of API response objects 

`full_data_access.py`: used to access the api and interact directly with notebook and repository metadata files in the **full** dataset, makes a number of changes compared to `data_access.py`, to make running more efficient on the bigger dataset:

- some functions make references to files instead of the API (dataset is on the feature server)

- uses `api_cache.py` to cache API response objects

`data_access.py`: used to access the api and interact directly with the notebook and repository metadata files in the dataset

`full_execute_all.py`: script to run all functions on the entire **full** dataset, outputting data in csv files (parallelized)

`execute_all.py`: script to run all functions on an entire dataset, outputs the data in csv files

### gathering the full dataset

`full_dataset_gathering.py`: gathers notebook data of the 143k notebook dataset into `full-dataset/notebooks.csv`

`full_path_gathering.py`: gathers the paths (repository) of each notebook in `notebooks.csv` (parallelized)

`gather_metadata.py`: gathers the repository metadata .json files for each repository in `full-dataset/repositories.csv` into a directory 

### feature scripts

`keyword_analysis.py`: searches the notebook markdown, code cells, and path for certain sets of keywords

`markdown_analysis.py`: does a variety of analysis on markdown cells in a notebook

`code_analysis.py`: does a variety of analysis on the code in a notebook

`notebook_analysis.py`: does a variety of analysis on a notebook file as a whole

`repo_analysis.py`: does a variety of analysis relating to the repository of the notebook

`regex.py`: various regular expressions used to detect links, equations, etc. in notebooks

`testing.py`: functionality to test all/single functions and compare results against manually detected features

## directory information

`full-dataset/`: includes .csv files pertaining to the full, 143k notebook dataset

`full-output`: includes the results of running `full_execute_all.py` on the full dataset

`output/`: includes the results of running `execute_all.py` on a dataset

`output/test-runs/`: results of test runs of running `execute_all.py` (for testing errors in scripts)

`output/complete-runs/`: results of complete runs of running `execute_all.py` (for actual data collection and analysis), also includes Jupyter notebooks that analyze the output for each complete run

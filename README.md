# quantifying-notebook-features

A collection of Python scripts to quantify and detect features of Jupyter notebooks. 

API Crawler from https://github.com/shuiblue/GitHubAPI-Crawler 

Testing dataset is a small subset from https://library.ucsd.edu/dc/object/bb2733859v

Created and used for Summer 2020 research on improving computational notebooks under Christian Kaestner and Shurui Zhou  at CMU ISR.

## file information

`data_access.py`: used to access the api and interact directly with the notebook and repository metadata files in the dataset
`keyword_analysis.py`: searches the notebook markdown, code cells, and path for certain sets of keywords
`markdown_analysis.py`: does a variety of analysis on markdown cells in a notebook
`notebook_analysis.py`: does a variety of analysis on a notebook file as a whole
`repo_analysis.py`: does a variety of analysis relating to the repository of the notebook

`testing.py`: functionality to test all/single functions and compare results against manually detected features
`execute_all.py`: script to run all functions on an entire dataset, outputs the data in csv files

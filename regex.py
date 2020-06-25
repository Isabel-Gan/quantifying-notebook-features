# a collection of regular expressions used throughout the scripts

# used to detect links in markdown cells
link = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"

# used to detect image insertion in markdown cells
img_src = "<img"

# used to detect equations (math mode)
equation = "\$([\S\s]+?)\$"

# regex associated with education notebooks
education = ["project", "hint", "rubric", "answer", "question", "pass",
                        "lesson", "lecture", "homework", "slides", "final-project",
                        "course", "assignment", "quiz", "submission","hw", "exercise", 
                        "due", "bootcamp", "assessment", "final_project",
                        "week([_\- ]|\B)([0-9]+)", "day([_\- ]|\B)([0-9]+)"]
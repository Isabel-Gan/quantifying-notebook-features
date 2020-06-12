import markdown_quant as md_quant 

nb_ids = [165313, 219322, 333748, 439119, 464706, 
            466289, 492523, 531968, 578489, 602217,
            681455, 884271, 958849, 972366, 972721,
            1019165, 1047986, 1051197, 1081631, 1124656]

# prints out the results of running a function on all notebooks
def test_func(func):
    for nb_id in nb_ids:
        print(str(nb_id) + " : " + str(func(nb_id)))

# PUT TESTS HERE
    
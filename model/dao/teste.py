from os.path import dirname, realpath

filepath = realpath(__file__)
print(filepath)
dir_of_file = dirname(filepath)
print(dir_of_file)
parent_dir_of_file = dirname(dir_of_file)
print(parent_dir_of_file)
parents_parent_dir_of_file = dirname(parent_dir_of_file)
print(parents_parent_dir_of_file)
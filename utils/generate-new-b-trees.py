# from btree import read_file_and_build_tree
from btreeJson import read_file_and_build_tree
from os.path import dirname, join

current_dir = dirname(__file__)
# users
# file_name = join(current_dir, "./users.csv")

## books
# file_name = join(current_dir, "./books.csv")

# ratings
file_name = join(current_dir, "./ratings.csv")

b_tree_data = read_file_and_build_tree(file_name)
b_tree_data.save_to_file(join(current_dir, "btree_data.bin"))

b_tree_data = read_file_and_build_tree(file_name)
b_tree_data = b_tree_data.save_to_file(join(current_dir, "btree.json"))
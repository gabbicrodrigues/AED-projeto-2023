# from btree import read_file_and_build_tree
from btree import read_file_and_build_tree
from os.path import dirname, join

current_dir = dirname(__file__)
# users
file_name = join(current_dir, "./db/users.csv")
b_tree_data = read_file_and_build_tree(file_name, 10000)
b_tree_data = b_tree_data.save_to_file(join(current_dir, "user_btree.json"))
## books
# file_name = join(current_dir, "./db/books.csv")
# b_tree_data = read_file_and_build_tree(file_name, 10000)
# b_tree_data = b_tree_data.save_to_file(join(current_dir, "rating_btree.json"))
# ratings
file_name = join(current_dir, "./db/ratings.csv")

b_tree_data = read_file_and_build_tree(file_name, 10000)
b_tree_data = b_tree_data.save_to_file(join(current_dir, "rating_btree.json"))
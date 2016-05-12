#Standard Modules
import sys
import os
import thread

#3rd Parties Modules


#Local Modules
import dirent_utils
import io_utils

import data_handler
import network



def input_files_parser(path):
	filepaths = []
	# else if the given path is a directory
	if dirent_utils.is_directory_exist(path):
		for sub_path in list_all_in_directory(path):
			filepaths.extend(input_files_parser(sub_path))
	# else if the given path is a file
	elif dirent_utils.is_file_exist(path):
		filepaths.append(path)

	return filepaths


def main():
	# there must be at least 3 argument
	# python main.py -c sample_comment.csv
	if len(sys.argv) < 3:
		io_utils.usage("python main.py [option] <data_filepath/directory>")

	comments_paths = []
	likeby_paths = []
	page_category_paths = []

	for index in range(1, len(sys.argv), 2):
		try:
			option = sys.argv[index]
			path = sys.argv[index + 1]

			if option == "-c":
				comments_paths.extend(input_files_parser(path))
			elif option == "-l":
				likeby_paths.extend(input_files_parser(path))
			elif option == "-p":
				page_category_paths.extend(input_files_parser(path))

		except IndexError:
			io_utils.usage("python main.py <option data_filepath/directory>")

	n = network.Network()

	# handle comments data
	if comments_paths:
		# thread.start_new_thread(n.comments_network_builder, tuple(comments_paths))
		n.comments_network_builder(comments_paths)

	if likeby_paths:
		# thread.start_new_thread(n.like_network_builder, tuple(likeby_paths))
		n.like_network_builder(likeby_paths)

	if page_category_paths:
		page_names, comments_data, size = data_handler.page_category_data_handler(page_category_paths)
		n.page_category_network_builder(page_names, comments_data, size)
	

if __name__ == '__main__':
	main()
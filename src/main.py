#Standard Modules
import sys
import os
import thread

#3rd Parties Modules


#Local Modules
import dirent_utils
import io_utils

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

def _help():
	print("Usage: python main.py [option] <data_filepath/directory>")


def main():
	# there must be at least 3 argument
	# python main.py -c sample_comment.csv
	if len(sys.argv) < 3:
		io_utils.usage("python main.py [option] <data_filepath/directory>", terminate = True)

	# container for file path
	comments_paths = []
	likeby_paths = []
	page_category_paths = []

	# plotting Mode
	page_post = False
	page_user = False
	post_user = False

	# setting variable
	min_threshold = 2

	index = 1


	# parse all options
	while(index < len(sys.argv)):
		try:
			option = sys.argv[index]
			if option == "-h" or option == "--help":
				_help()
			elif option == "-c" or option == "--comment":
				index += 1
				try:
					comments_paths.extend(input_files_parser(sys.argv[index]))
				except:
					io_utils.stderr("Dangling -c or --comment flag on command line\n", terminate = True)
			elif option == "-l" or option == "--like":
				index += 1
				try:
					likeby_paths.extend(input_files_parser(sys.argv[index]))
				except:
					io_utils.stderr("Dangling -l or --like flag on command line\n", terminate = True)
			# elif option == "-p" or option == "--page":
			# 	index += 1
			# 	try:
			# 		page_category_paths.extend(input_files_parser(sys.argv[index]))
			# 	except:
			# 		io_utils.stderr("Dangling -p or --page flag on command line\n", terminate = True)
			elif option == "-pp" or option == "--pagepost":
				page_post = True
			elif option == "-pu" or option == "--pageuser":
				page_user = True
			elif option == "-pr" or option == "--postuser":
				post_user = True
			elif option == "-m" or option == "--minthreshold":
				index += 1
				try:
					min_threshold = int(sys.argv[index])
				except:
					io_utils.stderr("Dangling -p or --page flag on command line\n", terminate = True)
			else:
				io_utils.stderr("Unsupported option: %s"%option, terminate = True)

			index += 1

		except IndexError:
			break

	n = network.Network(page_post, page_user, post_user, min_threshold = min_threshold)

	# handle comments data
	if comments_paths:
		# thread.start_new_thread(n.comments_network_builder, tuple(comments_paths))
		n.comments_network_builder(comments_paths)

	if likeby_paths:
	# 	# thread.start_new_thread(n.like_network_builder, tuple(likeby_paths))
		n.like_network_builder(likeby_paths)

	# if page_category_paths:
	# # 	page_names, comments_data, size = data_handler.page_category_data_handler(page_category_paths)
	# 	n.page_category_network_builder(page_names, comments_data, size)
	

if __name__ == '__main__':
	main()
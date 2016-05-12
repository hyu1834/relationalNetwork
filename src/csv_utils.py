#Standard Modules
import csv

#3rd Parties Modules


#Local Modules


def csv_parser(csv_filepath):
	# first make sure the file is a csv file


	# now prase the file
	# first create a csv reader object from a file pointer
	reader = csv.reader(open(csv_filepath, 'rb'), delimiter=',', quotechar='"')
	# reader is a iterable of every single row in the csv file.
	# since there isnt a general way of handling csv content, we will just return
	# the iterable here
	return reader

def csv_writer(csv_filepath, data):
	pass
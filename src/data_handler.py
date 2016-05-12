#Standard Modules


#3rd Parties Modules


#Local Modules
import csv_utils

PAGE_ID = 0
POST_ID = 1
_ID = 2
FB_ID = 3
PAGE_NAME = 4
FB_NAME = 5
MESSAGE = 6
TIME = 7

def data_praser(filepath):
	# container for the data
	data_by_page_id = {}
	data_by_post_id = {}
	data_by_fb_id = {}
	
	# now for every row in the csv file, organize it into the container
	data_content = csv_utils.csv_parser(filepath)
	content_headers =  data_content.next()
	for index, row in enumerate(data_content):
		# format the data in this form
		# {"page_id": {}}
		# "page_id","post_id","id","fb_id","page_name","fb_name","message","created_time"
		page_id = row[PAGE_ID]
		post_id = row[POST_ID]
		fb_id = row[FB_ID]
		_id = row[_ID]
		page_name = row[PAGE_NAME]
		fb_name = row[FB_NAME]
		message = row[MESSAGE:-1]
		time = row[-1:TIME]

		# handle page data
		if page_id in data_by_page_id:
			if post_id in data_by_page_id[page_id]:
				if fb_id in data_by_page_id[page_id][post_id]:
					data_by_page_id[page_id][post_id][fb_id].append((message, time))
				else:
					data_by_page_id[page_id][post_id][fb_id] = [(message, time)]
			else:
				data_by_page_id[page_id][post_id] = {fb_id: [(message, time)]}
		else:
			data_by_page_id[page_id] = {post_id: {fb_id: [(message, time)]}}


		#handle post data
		if page_id in data_by_post_id:
			if fb_id in data_by_post_id[post_id]["comments"]:
				data_by_post_id[post_id]["comments"][fb_id].append((message, time))
			else:
				data_by_post_id[post_id]["comments"][fb_id] = [(message, time)]
		else:
			data_by_post_id[post_id] = {"parent_post": post_id, "comments": {fb_id: [(message, time)]}}


		# handle data by fb_id
		if fb_id in data_by_fb_id:
			if page_id in data_by_fb_id[fb_id]:
				if post_id in data_by_fb_id[fb_id][page_id]:
					data_by_fb_id[fb_id][page_id][post_id].append((message, time))
				else:
					data_by_fb_id[fb_id][page_id][post_id] = [(message, time)]
			else:
				data_by_fb_id[fb_id][page_id] = {post_id: [(message, time)]}
		else:
			data_by_fb_id[fb_id] = {page_id: {post_id: [(message, time)]}}
		


	# return prased data
	return (data_by_page_id, data_by_post_id, data_by_fb_id)


def comments_data_handler(filepaths):
	# data container
	page_names = {}
	data = {}
	size = 0

	# extract all data from csv file(s)
	for filepath in filepaths:
		for index, row in enumerate(csv_utils.csv_parser(filepath)):
			if index == 0:
				continue
			size += 1
			page_id = row[0]
			post_id = row[1]
			_id = row[2]
			fb_id = row[3]
			page_name = row[4]
			fb_name = row[5]
			time = row[6]

			# store page name
			if not page_id in page_names:
				page_names[page_id] = page_name
				data[page_id] = {post_id: {fb_id: 1}}
				# structure the data into a dictionary
			else:
				if not post_id in data[page_id]:
					data[page_id][post_id] = {fb_id: 1}
				else:
					if not fb_id in data[page_id][post_id]:
						data[page_id][post_id][fb_id] = 1
					else:
						data[page_id][post_id][fb_id] += 1

	return (page_names, data, size)


def likeby_data_handler(filepaths):
	# data container
	page_names = {}
	data = {}
	size = 0
	# extract all data from csv file(s)
	for filepath in filepaths:
		for index, row in enumerate(csv_utils.csv_parser(filepath)):
			if index == 0:
				continue
			size += 1
			# "page_id","post_id","comment_id","fb_id","created_time"
			page_id = row[0]
			post_id = row[1]
			comment_id = row[2]
			fb_id = row[3]
			time = row[4]

			# store page name
			if not page_id in page_names:
				page_names[page_id] = page_id
				data[page_id] = {post_id: {comment_id: [fb_id]}}
				# structure the data into a dictionary
			else:
				if not post_id in data[page_id]:
					data[page_id][post_id] = {comment_id: [fb_id]}
				else:
					if not comment_id in data[page_id][post_id]:
						data[page_id][post_id][comment_id] = [fb_id]
					else:
						data[page_id][post_id][comment_id].append(fb_id)

	return page_names, data, size

def page_category_data_handler(filepaths):
	# data container
	page_names = {}
	data = {}
	size = 0
	# extract all data from csv file(s)
	for filepath in filepaths:
		for index, row in enumerate(csv_utils.csv_parser(filepath)):
			if index == 0:
				continue

			size += 1

	return page_names, data, size



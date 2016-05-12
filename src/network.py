#Standard Modules
import sys
import os

#3rd Parties Modules


#Local Modules
import dirent_utils
import io_utils
import csv_utils

import data_handler
import network_graph_tools as ngt


class Network(object):
	def __init__(self):
		pass

	def setup(self):
		pass

	# def comments_network_builder(self, page_names, comments_data, size):
	# 	# plot network by page
	# 	self.plot = ngt.Network_Graph()
	# 	self.plot.setup(size, size/2)

	# 	# container
	# 	edge_list = []
	# 	node_id = {}

	# 	for page_id, posts in comments_data.items():
	# 		# add a node by given page_id, and it size
	# 		self.plot.add_node(page_names[page_id], weight = len(posts)/1280*100, color = "red")
	# 		# first thing to do after adding a node is to save the node id
	# 		node_id[page_id] = self.plot.get_nodes_count() - 1
	# 		for post_id, users in posts.items():
	# 			# scale the node size based on the max user count
	# 			self.plot.add_node(post_id[-3:], weight = 40, color = "purple")
	# 			# first thing to do after adding a node is to save the node id
	# 			node_id[post_id] = self.plot.get_nodes_count() - 1
	# 			# create an edge between post and page
	# 			edge_list.append((node_id[page_id], node_id[post_id]))
	# 			for user_id, amount in users.items():
	# 				if user_id not in node_id:
	# 					# scale the node size based on the max user count
	# 					self.plot.add_node(user_id[-3:], weight = 1, color = "blue")
	# 					# first thing to do after adding a node is to save the node id
	# 					node_id[user_id] = self.plot.get_nodes_count() - 1
	# 				# create an edge between post and page
	# 				edge_list.append((node_id[post_id], node_id[user_id]))

	# 	# add all edges
	# 	self.plot.add_edges(edge_list)
	# 	# plot the graph as png
	# 	self.plot.plot_graph()	

	def comments_network_builder(self, filepaths):
		self.plot = ngt.Network_Graph()
		# container
		edge_list = []
		page_node_id = {}
		post_node_id = {}
		fb_node_id = {}
		data_size = 0

		# extract all data from csv file(s)
		for filepath in filepaths:
			for index, row in enumerate(csv_utils.csv_parser(filepath)):
				if index == 0:
					continue

				data_size += 1
				# "page_id","post_id","id","fb_id","page_name","fb_name","message","created_time"
				page_id = row[0]
				post_id = row[1]
				_id = row[2]
				fb_id = row[3]
				page_name = row[4]
				fb_name = row[5]
				time = row[6]


				if not page_id in page_node_id:
					self.plot.add_node(page_name, color = "red")
					page_node_id[page_id] = self.plot.get_nodes_count() - 1
				else:
					self.plot.update_node_size(page_node_id[page_id])

				if not post_id in post_node_id:
					self.plot.add_node(post_id[-3:], color = "blue")
					post_node_id[post_id] = self.plot.get_nodes_count() - 1
					edge_list.append((page_node_id[page_id], post_node_id[post_id]))
				else:
					self.plot.update_node_size(post_node_id[post_id])

				if not fb_id in fb_node_id:
					self.plot.add_node("", color = "lightblue")
					fb_node_id[fb_id] = self.plot.get_nodes_count() - 1
				else:
					self.plot.update_node_size(fb_node_id[fb_id])

				edge_list.append((fb_node_id[fb_id], post_node_id[post_id]))

		# get max size of each kind of node
		max_page_node_size = max([self.plot.get_node_size(_id) for _id in page_node_id.values()])
		max_post_node_size = max([self.plot.get_node_size(_id) for _id in post_node_id.values()])
		max_fb_node_size = max([self.plot.get_node_size(_id) for _id in fb_node_id.values()])

		for _id in page_node_id.values():
			self.plot.update_node_size(_id, size = self.plot.get_node_size(_id)/max_page_node_size*80)

		for _id in post_node_id.values():
			self.plot.update_node_size(_id, size = self.plot.get_node_size(_id)/max_post_node_size*70)

		for _id in fb_node_id.values():
			self.plot.update_node_size(_id, size = self.plot.get_node_size(_id)/max_fb_node_size*60)


		self.plot.setup(data_size, data_size/2)
		# add all edges
		self.plot.add_edges(list(set(edge_list)))
		# plot the graph as png
		self.plot.plot_graph()	

	def like_network_builder(self, filepaths):
		self.plot = ngt.Network_Graph()
		# container
		edge_list = []
		page_node_id = {}
		post_node_id = {}
		comment_node_id = {}
		fb_node_id = {}
		data_size = 0

		# extract all data from csv file(s)
		for filepath in filepaths:
			for index, row in enumerate(csv_utils.csv_parser(filepath)):
				if index == 0:
					continue

				data_size += 1
				# "page_id","post_id","id","fb_id","page_name","fb_name","message","created_time"
				page_id = row[0]
				post_id = row[1]
				comment_id = row[2]
				fb_id = row[3]
				time = row[4]


				if not page_id in page_node_id:
					self.plot.add_node(page_id[-4:], color = "red")
					page_node_id[page_id] = self.plot.get_nodes_count() - 1
				else:
					self.plot.update_node_size(page_node_id[page_id])

				if not post_id in post_node_id:
					self.plot.add_node(post_id[-3:], color = "blue")
					post_node_id[post_id] = self.plot.get_nodes_count() - 1
					edge_list.append((page_node_id[page_id], post_node_id[post_id]))
				else:
					self.plot.update_node_size(post_node_id[post_id])

				if not fb_id in fb_node_id:
					self.plot.add_node("", color = "lightblue")
					fb_node_id[fb_id] = self.plot.get_nodes_count() - 1

				if comment_id != "0":
					if not comment_id in comment_node_id:
						self.plot.add_node(post_id[-2:], color = "purple")
						comment_node_id[comment_id] = self.plot.get_nodes_count() - 1
					else:
						self.plot.update_node_size(comment_node_id[comment_id])

					edge_list.append((fb_node_id[fb_id], comment_node_id[comment_id]))
				else:
					edge_list.append((fb_node_id[fb_id], post_node_id[post_id]))

		# get max size of each kind of node
		max_page_node_size = max([self.plot.get_node_size(_id) for _id in page_node_id.values()])
		max_post_node_size = max([self.plot.get_node_size(_id) for _id in post_node_id.values()])
		max_comment_node_size = max([self.plot.get_node_size(_id) for _id in comment_node_id.values()])
		max_fb_node_size = max([self.plot.get_node_size(_id) for _id in fb_node_id.values()])

		for _id in page_node_id.values():
			self.plot.update_node_size(_id, size = self.plot.get_node_size(_id)/max_page_node_size*80)

		for _id in post_node_id.values():
			self.plot.update_node_size(_id, size = self.plot.get_node_size(_id)/max_post_node_size*70)

		for _id in comment_node_id.values():
			self.plot.update_node_size(_id, size = self.plot.get_node_size(_id)/max_comment_node_size*60)

		for _id in fb_node_id.values():
			self.plot.update_node_size(_id, size = self.plot.get_node_size(_id)/max_fb_node_size*50)


		self.plot.setup(20000, 10000)
		# add all edges
		self.plot.add_edges(list(set(edge_list)))
		# plot the graph as png
		self.plot.plot_graph()	

	def page_category_network_builder(self, page_names, page_data, size):
		self.plot = ngt.Network_Graph()
		
		# container
		edge_list = []
		node_id = {}

		# extract all data from csv file(s)
		for filepath in filepaths:
			for index, row in enumerate(csv_utils.csv_parser(filepath)):
				if index == 0:
					continue

		self.plot.setup()
		# add all edges
		self.plot.add_edges(list(set(edge_list)))
		# plot the graph as png
		self.plot.plot_graph()	





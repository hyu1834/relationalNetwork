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
	def __init__(self, page_post, page_user, post_user, min_threshold = 2):
		self.page_post = page_post
		self.page_user = page_user
		self.post_user = post_user
		self.min_threshold = min_threshold

	def setup(self):
		pass

	def scale_nodes(self, plot_instance, node_ids, exception, scale = 50.0):
		# determine the max post size
		max_page_records = max([plot_instance.get_node_size(_id) for _id in node_ids.values() if not _id in exception])
		# scale each post node size based on the max_page_records
		for _id in node_ids.values():
			plot_instance.update_node_size(_id, size = (float(plot_instance.get_node_size(_id))/float(max_page_records))*scale)

	def filter_meaningless_nodes_edges(self, plot_instance, node_ids, edge_list):
		# filtered out all duplicate edges
		edge_list = set(edge_list)
		# list of node to be remove
		remove_node_list = []
		# for every id in the node_id
		for _id in node_ids.values():
			# if the size is < threshold, then we put it in a remove list
			node_size = plot_instance.get_node_size(_id)
			# print(node_size)
			if node_size < self.min_threshold:
				# print(_id, node_size)
				remove_node_list.append(_id)
				# also take it out from the edge list
				edge_list = [edge for edge in edge_list if not _id in edge]

		return remove_node_list, edge_list

	def update_network(self, plot_instance, _id, _ids, name, color):
		# if current record page_id not seem anywhere before
		if not _id in _ids:
			# add the node to the plot, and store it id
			plot_instance.add_node(name, color = color)
			# store node id
			_ids[_id] = plot_instance.get_nodes_count() - 1
		else:	#else just update the size of the node
			plot_instance.update_node_size(_ids[_id])

		return _ids

	def plot_finalized_network(self, plot_instance, main_ids, sub_ids, edges_list):
		plot_instance.setup()
		# scale main_ids
		self.scale_nodes(plot_instance, main_ids, [])

		remove_node_list, edges_list = self.filter_meaningless_nodes_edges(plot_instance, sub_ids, edges_list)
		# scale page nodes size
		self.scale_nodes(plot_instance, sub_ids, remove_node_list)
		# add all edges
		plot_instance.add_edges(edges_list)
		# # scale the post node
		# self.scale_nodes(plot_instance, _ids)
		# node remove all useless node
		# DO NOT REMOVE NODE BEFORE ANYTHING
		original = plot_instance.get_nodes_count()
		plot_instance.remove_nodes(remove_node_list)
		print("Original network has: %s nodes, final network has: %s nodes"%(original, plot_instance.get_nodes_count()))
		# plot the graph as png
		plot_instance.plot_graph()	

		return edges_list

	def comments_network_builder(self, filepaths):
		if self.page_post:
			page_post_plot = ngt.Network_Graph()
			page_post_edge_list = []
			page_post_page_id = {}
			page_post_post_id = {}
			# page_post
		
		if self.page_user:
			page_user_plot = ngt.Network_Graph()
			page_user_edge_list = []
			page_user_page_id = {}
			page_user_user_id = {}

		if self.post_user:
			post_user_plot = ngt.Network_Graph()
			post_user_edge_list = []
			post_user_post_id = {}
			post_user_user_id = {}

		# read data files and construct network plot
		for filepath in filepaths:
			for index, row in enumerate(csv_utils.csv_parser(filepath)):
				# skip the header line
				if index == 0:
					continue

				# "","page_id","post_id","id","fb_id","page_name","fb_name","created_time"
				if len(row) == 8:
					record_index = row[0]
					page_id = row[1]
					post_id = row[2]
					_id = row[3]
					user_id = row[4]
					page_name = row[5]
					fb_name = row[6]
					time = row[7]
				elif len(row) == 7:
					page_id = row[0]
					post_id = row[1]
					_id = row[2]
					user_id = row[3]
					page_name = row[4]
					fb_name = row[5]
					time = row[6]


				if self.page_post:
					# try to add the node
					page_post_page_id = self.update_network(page_post_plot, page_id, page_post_page_id, page_name, "red")
					page_post_post_id = self.update_network(page_post_plot, post_id, page_post_post_id, post_id[-4:], "purple")
					# # if current record page_id not seem anywhere before
					# if not page_id in page_post_page_id:
					# 	# add the node to the plot, and store it id
					# 	page_post_plot.add_node(page_name, color = "red")
					# 	# store node id
					# 	page_post_page_id[page_id] = page_post_plot.get_nodes_count() - 1
					# else:	#else just update the size of the node
					# 	page_post_plot.update_node_size(page_post_page_id[page_id])

					# if not post_id in page_post_post_id:
					# 	page_post_plot.add_node(post_id[-4:], color = "purple")
					# 	page_post_post_id[post_id] = page_post_plot.get_nodes_count() - 1
					# else:	#else just update the size of the node
					# 	page_post_plot.update_node_size(page_post_post_id[post_id])

					page_post_edge_list.append((page_post_page_id[page_id], page_post_post_id[post_id]))

				if self.page_user:
					page_user_page_id = self.update_network(page_user_plot, page_id, page_user_page_id, page_name, "red")
					page_user_user_id = self.update_network(page_user_plot, user_id, page_user_user_id, user_id[-4:], "purple")
					# # if current record page_id not seem anywhere before
					# if not page_id in page_user_page_id:
					# 	# add the node to the plot, and store it id
					# 	page_user_plot.add_node(page_name, color = "red")
					# 	# store node id
					# 	page_user_page_id[page_id] = page_user_plot.get_nodes_count() - 1
					# else:	#else just update the size of the node
					# 	page_user_plot.update_node_size(page_user_page_id[page_id])

					# if not user_id in page_user_user_id:
					# 	page_user_plot.add_node(user_id[-4:], color = "purple")
					# 	page_user_user_id[user_id] = page_user_plot.get_nodes_count() - 1
					# else:	#else just update the size of the node
					# 	page_user_plot.update_node_size(page_user_user_id[user_id])

					page_user_edge_list.append((page_user_page_id[page_id], page_user_user_id[user_id]))
				
				if self.post_user:
					post_user_post_id = self.update_network(post_user_plot, post_id, post_user_post_id, post_id[-4:], "red")
					post_user_user_id = self.update_network(post_user_plot, user_id, post_user_user_id, user_id[-2:], "purple")
					# if not post_id in post_user_post_id:
					# 	post_user_plot.add_node(post_id[-4:], color = "purple")
					# 	post_user_post_id[post_id] = post_user_plot.get_nodes_count() - 1
					# else:	#else just update the size of the node
					# 	post_user_plot.update_node_size(post_user_post_id[post_id])

					# if not user_id in post_user_user_id:
					# 	post_user_plot.add_node(user_id[-2:], color = "purple")
					# 	post_user_user_id[user_id] = post_user_plot.get_nodes_count() - 1
					# else:	#else just update the size of the node
					# 	post_user_plot.update_node_size(post_user_user_id[user_id])

					post_user_edge_list.append((post_user_post_id[post_id], post_user_user_id[user_id]))


		if self.page_post:
			page_post_edge_list = self.plot_finalized_network(page_post_plot, page_post_page_id, page_post_post_id, page_post_edge_list)
			# page_post_plot.setup()
			# # scale page nodes size
			# self.scale_nodes(page_post_plot, page_post_page_id)
			# remove_node_list, page_post_edge_list = self.filter_meaningless_nodes_edges(page_post_plot, page_post_post_id, 
			# 																			page_post_edge_list)
			# # add all edges
			# page_post_plot.add_edges(page_post_edge_list)
			# # scale the post node
			# self.scale_nodes(page_post_plot, page_post_post_id)
			# # node remove all useless node
			# # DO NOT REMOVE NODE BEFORE ANYTHING
			# page_post_plot.remove_nodes(remove_node_list)
			# # plot the graph as png
			# page_post_plot.plot_graph()	

		if self.page_user:
			page_user_edge_list = self.plot_finalized_network(page_user_plot, page_user_page_id, page_user_user_id, page_user_edge_list)

			# page_user_plot.setup()
			# # scale page nodes size
			# self.scale_nodes(page_user_plot, page_user_page_id)
			# remove_node_list, page_user_edge_list = self.filter_meaningless_nodes_edges(page_user_plot, page_user_user_id, 
			# 																			page_user_edge_list)
			# # add all edges
			# page_user_plot.add_edges(page_user_edge_list)
			# # scale the post node
			# self.scale_nodes(page_user_plot, page_user_user_id)
			# # node remove all useless node
			# # DO NOT REMOVE NODE BEFORE ANYTHING
			# page_user_plot.remove_nodes(remove_node_list)
			# # plot the graph as png
			# page_user_plot.plot_graph()	
		
		if self.post_user:
			post_user_edge_list = self.plot_finalized_network(post_user_plot, post_user_post_id, post_user_user_id, post_user_edge_list)

			# post_user_plot.setup()
			# # scale page nodes size
			# self.scale_nodes(post_user_plot, post_user_post_id)
			# remove_node_list, post_user_edge_list = self.filter_meaningless_nodes_edges(post_user_plot, post_user_user_id, 
			# 																			post_user_edge_list)
			# # add all edges
			# post_user_plot.add_edges(post_user_edge_list)
			# # scale the post node
			# self.scale_nodes(post_user_plot, post_user_user_id)
			# # node remove all useless node
			# # DO NOT REMOVE NODE BEFORE ANYTHING
			# post_user_plot.remove_nodes(remove_node_list)
			# # plot the graph as png
			# post_user_plot.plot_graph()	



	def like_network_builder(self, filepaths):
		if self.page_post:
			page_post_plot = ngt.Network_Graph()
			page_post_edge_list = []
			page_post_page_id = {}
			page_post_post_id = {}
		
		if self.page_user:
			page_user_plot = ngt.Network_Graph()
			page_user_edge_list = []
			page_user_page_id = {}
			page_user_user_id = {}

		if self.post_user:
			post_user_plot = ngt.Network_Graph()
			post_user_edge_list = []
			post_user_post_id = {}
			post_user_user_id = {}

		# read data files and construct network plot
		for filepath in filepaths:
			for index, row in enumerate(csv_utils.csv_parser(filepath)):
				# skip the header line
				if index == 0:
					continue

				# "","page_id","post_id","comment_id","fb_id","created_time"
				if len(row) == 6:
					record_index = row[0]
					page_id = row[1]
					post_id = row[2]
					comment_id = row[3]
					user_id = row[4]
					time = row[5]
				elif len(row) == 5:
					page_id = row[0]
					post_id = row[1]
					comment_id = row[2]
					user_id = row[3]
					time = row[4]


				if self.page_post:
					# try to add the node
					page_post_page_id = self.update_network(page_post_plot, page_id, page_post_page_id, page_id[-4:], "red")
					page_post_post_id = self.update_network(page_post_plot, post_id, page_post_post_id, page_id[-2:], "purple")
					page_post_edge_list.append((page_post_page_id[page_id], page_post_post_id[post_id]))

				if self.page_user:
					page_user_page_id = self.update_network(page_user_plot, page_id, page_user_page_id, page_name, "red")
					page_user_user_id = self.update_network(page_user_plot, user_id, page_user_user_id, user_id[-4:], "purple")
					page_user_edge_list.append((page_user_page_id[page_id], page_user_user_id[user_id]))
				
				if self.post_user:
					post_user_post_id = self.update_network(post_user_plot, post_id, post_user_post_id, post_id[-4:], "red")
					post_user_user_id = self.update_network(post_user_plot, user_id, post_user_user_id, user_id[-2:], "purple")
					post_user_edge_list.append((post_user_post_id[post_id], post_user_user_id[user_id]))


		if self.page_post:
			page_post_edge_list = self.plot_finalized_network(page_post_plot, page_post_page_id, page_post_post_id, page_post_edge_list)

		if self.page_user:
			page_user_edge_list = self.plot_finalized_network(page_user_plot, page_user_page_id, page_user_user_id, page_user_edge_list)
		
		if self.post_user:
			post_user_edge_list = self.plot_finalized_network(post_user_plot, post_user_post_id, post_user_user_id, post_user_edge_list)

	def page_category_network_builder(self, page_names, page_data, size):
		if self.page_post:
			page_post_plot = ngt.Network_Graph()
			page_post_edge_list = []
			page_post_page_id = {}
			page_post_post_id = {}
		
		if self.page_user:
			page_user_plot = ngt.Network_Graph()
			page_user_edge_list = []
			page_user_page_id = {}
			page_user_user_id = {}

		if self.post_user:
			post_user_plot = ngt.Network_Graph()
			post_user_edge_list = []
			post_user_post_id = {}
			post_user_user_id = {}

		# read data files and construct network plot
		for filepath in filepaths:
			for index, row in enumerate(csv_utils.csv_parser(filepath)):
				# skip the header line
				if index == 0:
					continue

				# "","page_id","post_id","id","fb_id","page_name","fb_name","created_time"
				record_index = row[0]
				page_id = row[1]
				post_id = row[2]
				_id = row[3]
				fb_id = row[4]
				page_name = row[5]
				fb_name = row[6]
				time = row[7]


				if self.page_post:
					pass

				if self.page_user:
					pass
				
				if self.post_user:
					pass


		if self.page_post:
			page_post_plot.setup()
			# add all edges
			page_post_plot.add_edges(list(set(page_post_edge_list)))
			# plot the graph as png
			page_post_plot.plot_graph()	

		if self.page_user:
			page_user_plot.setup()
			# add all edges
			page_user_plot.add_edges(list(set(page_user_edge_list)))
			# plot the graph as png
			page_user_plot.plot_graph()	
		
		if self.post_user:
			post_user_plot.setup()
			# add all edges
			post_user_plot.add_edges(list(set(post_user_edge_list)))
			# plot the graph as png
			post_user_plot.plot_graph()	





#Standard Modules


#3rd Parties Modules
import igraph

#Local Modules


class Network_Graph(object):
	def __init__(self):
		# create a graph from igraph
		self.graph = igraph.Graph()

		# graph style
		self.visual_style = {}


	def setup(self, height = 1280, width = 800):
		# Set bbox and margin
		self.visual_style["bbox"] = (height, width)
		self.visual_style["margin"] = 20
		self.visual_style["edge_width"] = 1
		# self.visual_style["vertex_size"] = 0
		# self.visual_style["layout"] = "circle"
		# Don't curve the edges
		self.visual_style["edge_curved"] = False

	def update_node_size(self, _id, size = -1):
		if size == -1:
			self.visual_style["vertex_size"][_id] += 1
		else:
			self.visual_style["vertex_size"][_id] = size

	def get_node_size(self, _id):
		return self.visual_style["vertex_size"][_id]

	def add_node(self, vertices_name, color = None):
		# self.graph.vs["name"].append(vertices_name)
		self.graph.add_vertex()
		# set the name of the versity
		self.graph.vs[self.get_nodes_count()-1]["label"] = vertices_name
		if not "vertex_size" in self.visual_style:
			self.visual_style["vertex_size"] = [1]
		else:
			self.visual_style["vertex_size"].append(1)

		if color:
			if not "vertex_color" in self.visual_style:
				self.visual_style["vertex_color"] = [color]
			else:
				self.visual_style["vertex_color"].append(color)

	def remove_node(self):
		pass

	def add_edge(self, source, dest):
		self.graph.add_edges([(source, dest)])
		
	def add_edges(self, edges_list):
		self.graph.add_edges(edges_list)

	def remove_edge(self):
		pass

	def get_nodes_count(self):
		return len(self.graph.vs)

	def get_edges_count(self):
		return len(self.graph.es)

	def plot_graph(self):
		if self.visual_style:
			# finally graph it
			igraph.plot(self.graph, **self.visual_style)
		else:
			igraph.plot(self.graph)
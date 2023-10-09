import wx
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class GraphPanel(wx.Panel):
    def __init__(self, parent, graph):
        wx.Panel.__init__(self, parent)
        # set size of the panel
        self.SetSize((800, 600))
        self.graph = graph
        # or use a random layout
        # create the figure and canvas for the graph
        self.figure = Figure(figsize=(8, 6), dpi=125)
        # make it bigger than the default size
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)

        # set the node positions using kamada_kawai_layout with high scale
        self.pos = nx.kamada_kawai_layout(self.graph, scale=10.0) # or use a random layout
        # self.pos = nx.random_layout(self.graph, scale=10.0)
        # self.pos = nx.circular_layout(self.graph, scale=10.0)
        # self.pos = nx.spring_layout(self.graph, scale=10.0)
        # self.pos = nx.spectral_layout(self.graph, scale=10.0)
        # self.pos = nx.shell_layout(self.graph, scale=10.0)
        # self.pos = nx.bipartite_layout(self.graph, scale=10.0)
        # self.pos = nx.fruchterman_reingold_layout(self.graph, scale=10.0)
        # self.pos = nx.spiral_layout(self.graph, scale=10.0)
        # self.pos = nx.multipartite_layout(self.graph, scale=10.0) # needs subset
        # self.pos = nx.rescale_layout(self.graph, scale=10.0)
        # self.pos = nx.planar_layout(self.graph, scale=10.0)
        # draw the graph with adjusted node size
        self.draw()

        # make the nodes draggable
        self.cid = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.rid = None

        # create a sizer for the panel and add the canvas to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def draw(self):
        # clear the figure and draw the graph
        self.axes.clear()
        nx.draw_networkx(self.graph, pos=self.pos, ax=self.axes, with_labels=True, 
                        node_color="white", linewidths=1, edgecolors="black",
                        edge_color='grey', font_size=8, font_color='black', 
                        font_weight='light', width=1, alpha=0.8, arrows=True, 
                        style='solid', labels=None, arrowsize=10, arrowstyle='-|>',
                        node_shape='o', min_source_margin=10, min_target_margin=10,
                        edge_cmap=None, edge_vmin=None, edge_vmax=None,
                        node_size=[len(n) * 75 for n in self.graph.nodes()]) # adjusted node size

        self.canvas.draw()

    def on_press(self, event):
        if event.inaxes is None:
            return
        node = None
        for n in self.graph.nodes:
            # check if the mouse click is on a node
            if abs(self.pos[n][0] - event.xdata) < 0.3 and abs(self.pos[n][1] - event.ydata) < 0.3:
                node = n
                break
        if node is not None:
            # set the current node to be draggable
            self.canvas.mpl_disconnect(self.cid)
            self.cid = self.canvas.mpl_connect('motion_notify_event', lambda event: self.on_motion(event, node))
            self.rid = self.canvas.mpl_connect('button_release_event', lambda event: self.on_release(event, node))

    def on_motion(self, event, node):
        # update the position of the node if it's not None
        if event.xdata is not None and event.ydata is not None:
            self.pos[node] = (event.xdata, event.ydata)
        # redraw the graph with the new node position
        self.draw()
        # draw the node at its new position
        self.axes.scatter(self.pos[node][0], self.pos[node][1], s=1000, color='red', alpha=0.5)
        self.canvas.draw()

    def on_release(self, event, node):
        # disconnect the motion and release events
        self.canvas.mpl_disconnect(self.cid)
        self.canvas.mpl_disconnect(self.rid)
        # connect the button press event again
        self.cid = self.canvas.mpl_connect('button_press_event', self.on_press)
        # redraw the graph without the red node
        self.draw()

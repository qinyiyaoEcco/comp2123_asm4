from Vertex import Vertex

"""
Graph Class
----------

This class represents the Graph modelling our courier network. 

Each Graph consists of the following properties:
    - vertices: A list of vertices comprising the graph

The class also supports the following functions:
    - add_vertex(vertex): Adds the vertex to the graph
    - remove_vertex(vertex): Removes the vertex from the graph
    - add_edge(vertex_A, vertex_B): Adds an edge between the two vertices
    - remove_edge(vertex_A, vertex_B): Removes an edge between the two vertices
    - send_message(s, t): Returns a valid path from s to t containing at most one untrusted vertex
    - check_security(s, t): Returns the set of edges that, if any are removed, would result in any s-t path having to use an untrusted edge

Your task is to complete the following functions which are marked by the TODO comment.
Note that your modifications to the structure of the Graph should be correctly updated in the underlying Vertex class!
You are free to add properties and functions to the class as long as the given signatures remain identical.
"""


class Graph():
    # These are the defined properties as described above
    vertices: 'list[Vertex]'

    def __init__(self) -> None:
        """
        The constructor for the Graph class.
        """
        self.vertices = []

    def add_vertex(self, vertex: Vertex) -> None:
        """
        Adds the given vertex to the graph.
        If the vertex is already in the graph or is invalid, do nothing.
        :param vertex: The vertex to add to the graph.
        """

        if vertex in self.vertices:
            return
        self.vertices.append(vertex)

        # TODO Fill this in

    def remove_vertex(self, vertex: Vertex) -> None:
        """
        Removes the given vertex from the graph.
        If the vertex is not in the graph or is invalid, do nothing.
        :param vertex: The vertex to remove from the graph.
        """
        if vertex not in self.vertices:
            return
        self.vertices.remove(vertex)

        # TODO Fill this in

    def add_edge(self, vertex_A: Vertex, vertex_B: Vertex) -> None:
        """
        Adds an edge between the two vertices.
        If adding the edge would result in the graph no longer being simple or the vertices are invalid, do nothing.
        :param vertex_A: The first vertex.
        :param vertex_B: The second vertex.
        """
        vertex_A.add_edge(vertex_B)
        # TODO Fill this in

    def remove_edge(self, vertex_A: Vertex, vertex_B: Vertex) -> None:
        """
        Removes an edge between the two vertices.
        If an existing edge does not exist or the vertices are invalid, do nothing.
        :param vertex_A: The first vertex.
        :param vertex_B: The second vertex.
        """
        vertex_A.remove_edge(vertex_B)
        # TODO Fill this in

    def Dijkstra(self, s: Vertex, t: Vertex):
        visited = {}
        for vertex in self.vertices:
            visited[vertex] = False
        weight = {s: 0}
        pre = {s: None}
        min_heap = [s]
        while len(min_heap) > 0:
            min_heap.sort(key=lambda x: weight[x])
            tmp = min_heap.pop(0)
            visited[tmp] = True

            for adj in tmp.edges:
                if not visited[adj]:
                    if adj.get_is_trusted():
                        wei = 0
                    elif tmp.get_is_trusted():
                        wei = 1
                    else:
                        wei= 1 if type(weight[tmp]) is float else 1.5

                    if adj not in weight:  # 如果是新来的
                        pre[adj] = tmp
                        weight[adj] = weight[tmp] + wei
                        min_heap.append(adj)
                    elif weight[tmp] + wei < weight[adj]:  # 如果已经在堆里
                        pre[adj] = tmp
                        weight[adj] = weight[tmp] + wei
        return pre, weight

    def send_message(self, s: Vertex, t: Vertex) -> 'list[Vertex]':
        """
        Returns a valid path from s to t containing at most one untrusted vertex.
        Any such path between s and t satisfying the above condition is acceptable.
        Both s and t can be assumed to be unique and trusted vertices.
        If no such path exists, return None.
        :param s: The starting vertex.
        :param t: The ending vertex.
        :return: A valid path from s to t containing at most one untrusted vertex.
        """
        path = [s]
        pre, weight = self.Dijkstra(s, t)
        if t in weight and weight[t] <= 1:
            while pre[t] != None:
                path.insert(1, t)
                t = pre[t]
            return path
        else:
            return None

    def check_security(self, s: Vertex, t: Vertex) -> 'list[(Vertex, Vertex)]':
        """
        Returns the list of edges as tuples of vertices (v1, v2) such that the removal 
        of the edge (v1, v2) means a path between s and t is not possible or must use
        two or more untrusted vertices in a row. v1 and v2 must also satisfy the criteria
        that exactly one of v1 or v2 is trusted and the other untrusted.        
        Both s and t can be assumed to be unique and trusted vertices.
        :param s: The starting vertex
        :param t: The ending vertex
        :return: A list of edges which, if removed, means a path from s to t uses an untrusted edge or is no longer possible. 
        Note these edges can be returned in any order and are unordered.
        """
        # 获取所有half_path
        half_path = []
        for v in self.vertices:
            for e in v.edges:
                if (v.get_is_trusted() or e.get_is_trusted()) and (not v.get_is_trusted() or not e.get_is_trusted()):
                    if (v, e) not in half_path and (e, v) not in half_path:
                        half_path.append((v, e))

        for l, r in half_path.copy():
            self.remove_edge(l, r)
            pre, weight = self.Dijkstra(s, t)
            if t in weight and type(weight[t]) is int:
                half_path.remove((l, r))
            self.add_edge(l, r)

        return half_path
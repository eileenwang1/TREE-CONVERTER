class Semantics(list):
    def __init__(self,idx):
        self.idx = idx

    def is_in(self,new,branch=""):
        new = new.strip()
        # this is not a branching tree
        if len(self)==0 or not isinstance(self[-1],list):
            for i in range(len(self)):
                self[i] = self[i].strip()
                if self[i] == new:
                    return True
            return False
        
        # this is a branching tree
        if branch=="":
            # branch is not specified
            for i in range(len(self)):
                if not isinstance(self[-1],list):
                    self[i] = self[i].strip()
                    if self[i]==new:
                        return True
                else:
                    if self[i].is_in(new)==True:
                        return True
            return False

        # branch is specified
        for i in range(len(self)-2):
            if not isinstance(self[-1],list):
                self[i] = self[i].strip()
                if self[i]==new:
                    return True
            else:
                raise Exception("list element at index {}".format(i))
        if branch[0]=='l':
            self[-2].is_in(new,branch[1:])
        elif branch[0]=='r':
            self[-1].is_in(new,branch[1:])
        else:
            raise Exception("wrong branch encoding {}".format(branch))


    def append(self,new,branch=""):
        # if branch is not specified
        if branch == "":
            if len(self)==0 or not isinstance(self[-1],list):
                if not isinstance(new,list):
                    if not Semantics.is_in(self,new,branch):
                        return list.append(self,new)
                    return 
                else:
                    for i in new:
                        list.append(self,[i])
                    return
            else:
                # if the tree has branches
                # find the number of branchs
                counter = 0
                for i in range(1,len(self)+1):
                    if isinstance(self[0-i],list):
                        counter += 1
                # print("counter: ",counter)
                if not isinstance(new,list):
                    for i in range (1,counter+1):
                        Semantics.append(self[0-i],new,branch)
                    return
                else:
                    for i in range(1,counter+1):
                        Semantics.append(self[0-i],new,branch)
                    return 
        else:
            # if there is not a branch
            if (len(self)<2) or (not isinstance(self[-2],list)) or (not isinstance(self[-1],list)):
                list.append(self,[])
                list.append(self,[])
                # print("after append")
                # print(self)
            # if branch is specified
            if branch[0]=='l':
                try:
                    return Semantics.append(self[-2],new,branch[1:])
                except:
                    print(self)
                # return Semantics.append(self[-2],new,branch[1:])
                
            elif branch[0]=='r':
                return Semantics.append(self[-1],new,branch[1:])
            else:
                raise Exception("wrong branch encoding {}".format(branch))

    def path(self,branch=""):
        # return a list of paths
        to_return = [[]]
        for i in range(len(self)):
            if not isinstance(self[i],list):
                to_return[0].append(self[i])
            else:
                if branch == 'l':
                    return [to_return[0] + Semantics.path(self[i],branch[1:])]
                elif branch =='r':
                    return [to_return[0] + Semantics.path(self[i+1],branch[1:])]
                elif branch=='':
                    return [to_return[0] + Semantics.path(self[i],branch[1:]),to_return + Semantics.path(self[i+1],branch[1:])]
                else:
                    raise Exception("wrong info in branch")
        return to_return
                    

# from Data Structures, Spring 2019
class Graph:
    """Representation of a simple graph using an adjacency map."""

    #------------------------- nested Vertex class -------------------------
    class Vertex:
        """Lightweight vertex structure for a graph."""
        # __slots__ = '_element'
    
        def __init__(self, idx, semantics=[]):
            """Do not call constructor directly. Use Graph's insert_vertex(x)."""
            self.idx = idx
            self.semantics = Semantics(idx)
            self.contradiction = False
        # def element(self):
        #     """Return element associated with this vertex."""
        #     return self._element
    
        def __hash__(self):         # will allow vertex to be a map/set key
            return hash(self.idx)

        def __str__(self):
            return "VERTEX ({}, {})".format(self.idx,self.semantics)
            # return str(self.goal)

        def __repr__(self):
            return "VERTEX ({}, {})".format(self.idx,self.semantics)

        def __ge__(self,v2):
            if not isinstance(v2,type(self)):
                raise ValueError("not a vertex to compare")
            return self.idx >= v2.idx
        
        def __eq__(self,v2):
            if not isinstance(v2,type(self)):
                raise ValueError("not a vertex to compare")
            return self.idx==v2.idx and self.semantics==v2.semantics


            # return str(self.goal)
        
    #------------------------- nested Edge class -------------------------
    class Edge:
        """Lightweight edge structure for a graph."""
        # __slots__ = '_origin', '_destination', '_element'
    
        def __init__(self, u, v, branch=""):
            """Do not call constructor directly. Use Graph's insert_edge(u,v,x)."""
            self._origin = u
            self._destination = v
            self.branch = branch    # in the case of branching worlds, self.branch = 'l' or 'r'
    
        def endpoints(self):
            """Return (u,v) tuple for vertices u and v."""
            return (self._origin, self._destination)
    
        def opposite(self, v):
            """Return the vertex that is opposite v on this edge."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v must be a Vertex')
            return self._destination if v is self._origin else self._origin
            raise ValueError('v not incident to edge')
    
        # def element(self):
        #     """Return element associated with this edge."""
        #     return self._element
    
        def __hash__(self):         # will allow edge to be a map/set key
            return hash( (self._origin, self._destination) )

        def __str__(self):
            return '({0},{1},{2},{3})'.format(self._origin,self._destination,self.rule_encoding,self.matching_dict)

        def __repr__(self):
            if self._origin.idx < self._destination.idx:
                u = self._origin
                v = self._destination
            else:
                u = self._destination
                v = self._origin
            return 'EDGE: ({0},{1},{2},{3})'.format(u,v,self.rule_encoding,self.matching_dict)
        
    #------------------------- Graph methods -------------------------
    def __init__(self, directed=False):
        """Create an empty graph (undirected, by default).

        Graph is directed if optional parameter is set to True.
        """
        self._outgoing = {}
        # only create second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing

    def __str__(self):
        def edge_key(e):
            if e._origin.idx < e._destination.idx:
                u = e._origin
                v = e._destination
            else:
                u = e._destination
                v = e._origin
            return u.idx
                
        edges = list(self.edges())
        sorted_edges = sorted(edges,key=lambda x:edge_key(x))
        result = []
        for each in sorted_edges:
            result.append(str(each) + "\n")
        return "".join(result)
    
    def size(self):
        return len(self.vertices())
    
    def dfs(self,start_node):
        # retrun an iteration in the dfs order
        def dfs_inner(start_node,visited):
            visited.append(start_node)
            adj_list = list(self._outgoing[start_node].keys())
            for i in range(len(adj_list)):
                has_visited = False
                for j in visited:
                    if j == adj_list[i]:
                        has_visited = True
                        break
                if not has_visited:
                    dfs_inner(adj_list[i],visited)
            return visited

        if len(self._outgoing)==0:
            return []
        to_return = dfs_inner(start_node,[])
        return to_return

    def _validate_vertex(self, v):
        """Verify that v is a Vertex of this graph."""
        if not isinstance(v, self.Vertex):
            raise TypeError('Vertex expected')
        if v not in self._outgoing:
            raise ValueError('Vertex does not belong to this graph.')
        
    def is_directed(self):
        """Return True if this is a directed graph; False if undirected.

        Property is based on the original declaration of the graph, not its contents.
        """
        return self._incoming is not self._outgoing # directed if maps are distinct

    def vertex_count(self):
        """Return the number of vertices in the graph."""
        return len(self._outgoing)

    def vertices(self):
        """Return an iteration of all vertices of the graph."""
        return list(self._outgoing.keys())

    def edge_count(self):
        """Return the number of edges in the graph."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # for undirected graphs, make sure not to double-count edges
        return total if self.is_directed() else total // 2

    def edges(self):
        """Return a set of all edges of the graph."""
        result = set()       # avoid double-reporting edges of undirected graph
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())    # add edges to resulting set
        return result

    def get_edge(self, u, v):
        """Return the edge from u to v, or None if not adjacent."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)        # returns None if v not adjacent

    def degree(self, v, outgoing=True):   
        """Return number of (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to count incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):   
        """Return all (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to request incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self):
        """Insert and return a new Vertex with element x."""
        idx = len(self._outgoing)
        v = self.Vertex(idx)  #create a new instance in the vertex class
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}        # need distinct map for incoming edges
        return v
            
    def insert_edge(self, u, v, branch = ""):
        """Insert and return a new Edge from u to v with auxiliary element x.

        Raise a ValueError if u and v are not vertices of the graph.
        Raise a ValueError if u and v are already adjacent.
        """
        if self.get_edge(u, v) is not None:      # includes error checking
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, branch)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e

    def find_root(self):
        if self.size()==0:
            return None
        return self.idx_to_vertex(0)
    
    def idx_to_vertex(self,idx):
        # input: idx of a vertex
        # return the vertex
        if len(self._outgoing)==0 or idx>=len(self._incoming):
            raise ValueError('vertex DNE')
        for i in self._outgoing.keys():
            if i.idx==idx:
                return i
        return None
        # raise ValueError('vertex DNE')
    
    def path_length(self, destination, source=None):
        if source==None:
            source = self.idx_to_vertex(0)
        return self.bfs(destination,source,0)

    def bfs(self,destination,source,curr_distance):
        adj_list = list(self._outgoing[source].keys())
        if len(adj_list)==0:
            return -1
            # deadend, there is no path between 2 nodes
        for i in range(len(adj_list)):
            if adj_list[i]==destination:
                return curr_distance+1
        for i in range(len(adj_list)):
            return self.bfs(destination,adj_list[i],curr_distance+1)

        

        
    # def goal_to_vertex(self,goal):
    #     # input: goal of a vertex
    #     # return the vertex
    #     if len(self._outgoing)==0:
    #         print("GOAL: ",goal)
    #         raise ValueError('vertex DNE')
    #     for i in self._outgoing.keys():
    #         if i.goal==goal:
    #             return i
    #     return None
    #     # raise ValueError('vertex DNE')

    # def encoding_to_edge(self,rule_encoding):
    #     # input: encoding of a edge
    #     # return :the corresponding edge if the edge exists, none otherwise
    #     edges = list(self.edges())
    #     for i in range(len(edges)):
    #         if edges[i].rule_encoding==rule_encoding:
    #             return edges[i]
    #     return None
    
    # def first_vertex_without_goal(self):
    #     # return the vertex with the smallest idx that is without goal
    #     vertices=sorted(self.vertices(), key = lambda u: u.idx)
    #     for i in range(len(vertices)):
    #         if vertices[i].goal==None or vertices[i].goal=="":
    #             return vertices[i]
    #     return None
    
    # def incoming_edge(self,v):
    #     # find the edge that connects v to a vertex of smaller idx
    #     incident_edges = self.incident_edges(v)
    #     incident_edges = list(incident_edges)
    #     curr_idx = v.idx
    #     curr_edge = None
    #     for i in range(len(incident_edges)):
    #         u,v = incident_edges[i].endpoints()
    #         if u.idx<=curr_idx and v.idx<=curr_idx:
    #             curr_edge = incident_edges[i]
    #             return curr_edge
    #     return curr_edge

                
# a = Semantics(0)
# a.append("a")
# print(a)
# print(len(a))
# a.append(["b","c"])
# print(a)
# print(len(a))
# a.append("d")
# print(a)
# print(len(a))
# a.append(["e","f"])
# print(a)
# print(len(a))
# a.append("g")
# print(a)
# print(len(a))

# g = Graph()
# g.insert_vertex(1)
# g.insert_vertex(2)
# g.insert_vertex(0)
# g.idx_to_vertex(1).syntax = [4,5,6]
# print(type(g.idx_to_vertex(1).semantics))
# g.idx_to_vertex(1).semantics.append("hello")
# g.idx_to_vertex(2).semantics.append(["this is rediculous","hi"])
# g.idx_to_vertex(0).semantics.append("hey")

# for i in range(3):
#     print(g.idx_to_vertex(i).semantics)











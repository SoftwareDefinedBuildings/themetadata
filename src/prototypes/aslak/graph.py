from abc import abstractmethod

# TODO: ports = (direction?, incoming edges, outgoing edges)

class Node:
    @abstractmethod
    def add_incoming (edge, port):
        return
    
    @abstractmethod
    def add_outgoing (edge, port):
        return

class PrimitiveNode(Node):
    def __init__ (self, attrs={}, nodelist=None):
        self.attrs = attrs
        
        self.incoming = []
        self.outgoing = []
        
        if nodelist: nodelist.append(self)
    
    def add_incoming(self, edge, port): self.incoming.append(edge)
    def add_outgoing(self, edge, port): self.outgoing.append(edge)

class ComplexNode(Node):
    def __init__ (self, nodes, edges, incoming_portmap, outgoing_portmap, attrs={}, nodelist=None):
        self.nodes = nodes
        self.edges = edges
        self.attrs = attrs
        
        # ports for incoming edges
        self.incoming = {}
        for port in incoming_portmap:
            self.incoming[port] = {
                'inside':  incoming_portmap[port],
                'outside': []
            }
        
        # ports for outgoing edges
        self.outgoing = {}
        for port in outgoing_portmap:
            self.outgoing[port] = {
                'inside':  outgoing_portmap[port],
                'outside': []
            }
        
        if nodelist: nodelist.append(self)
    
    def add_incoming(self, edge, port): self.incoming[port]['outside'].append(edge)
    def add_outgoing(self, edge, port): self.outgoing[port]['outside'].append(edge)

class Edge:
    def __init__ (self, edgetype, src, dst, src_port=None, dst_port=None, attrs={}, edgelist=None):
        self.edgetype = edgetype
        self.src = src
        self.dst = dst
        self.src_port = src_port
        self.dst_port = dst_port
        self.attrs = attrs
        
        src.add_outgoing(self, src_port)
        dst.add_incoming(self, dst_port)
        
        if edgelist: edgelist.append(self)
    
    def primitive_src (self): return self.src_port == None
    def primitive_dst (self): return self.dst_port == None
    def complex_src (self): return not self.primitive_src()
    def complex_dst (self): return not self.primitive_dst()




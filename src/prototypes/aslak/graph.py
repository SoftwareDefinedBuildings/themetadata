from abc import abstractmethod

class Node:
    @abstractmethod
    def add_incoming (edge, port):
        return
    
    @abstractmethod
    def add_outgoing (edge, port):
        return

class PrimitiveNode (Node):
    def __init__ (self, attrs={}, nodelist=None):
        self.attrs = attrs
        
        self.incoming = []
        self.outgoing = []
        
        if nodelist != None:
            nodelist.append(self)
    
    def add_incoming (self, edge, port): self.incoming.append(edge)
    def add_outgoing (self, edge, port): self.outgoing.append(edge)

class ComplexNode (Node):
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
        
        if nodelist != None: nodelist.append(self)
    
    def add_incoming (self, edge, port): self.incoming[port]['outside'].append(edge)
    def add_outgoing (self, edge, port): self.outgoing[port]['outside'].append(edge)
    
    def as_dot (self, lines, nodemap, counter, indent=''):
        def escape_port (port): return port.replace(' ', '_')
        
        # guard: cyclic
        if self in nodemap: return
        
        # head
        nodemap[self] = 'node'+str(counter[0])
        counter[0] += 1
        lines.append(indent+'subgraph '+nodemap[self]+' {')
        lines.append(indent+'  label = "'+self.attrs['name']+'";')
        
        # true nodes
        for node in self.nodes:
            if not node in nodemap:
                if type(node)==ComplexNode:
                    node.as_dot(lines, nodemap, counter, indent+'  ')
                else:
                    nodemap[node] = 'node'+str(counter[0])
                    counter[0] += 1
                    lines.append(indent+'  '+nodemap[node]+' [color=black, label="'+node.attrs['name']+'"];')
        
        # port nodes
        for port in list(self.incoming.keys()) + list(self.outgoing.keys()):
            lines.append(indent+'  '+nodemap[self]+'_'+escape_port(port)+' [color=blue, label="'+port+'"];')
        
        # edges
        for edge in self.edges:
            name1 = nodemap[edge.src] + ('' if edge.primitive_src() else '_'+escape_port(edge.src_port))
            name2 = nodemap[edge.dst] + ('' if edge.primitive_dst() else '_'+escape_port(edge.dst_port))
            color = 'black' if edge.primitive_src() and edge.primitive_dst() else 'blue'
            lines.append(indent+'  '+name1+' -> '+name2+' [color='+color+'];')
        
        # port edges
        for port in self.incoming:
            for dst in self.incoming[port]['inside']:
                name1 = nodemap[self]+'_'+escape_port(port)
                name2 = nodemap[dst['node']] + ('_'+escape_port(dst['port']) if 'port' in dst else '')
                lines.append(indent+'  '+name1+' -> '+name2+' [color=blue];')
        for port in self.outgoing:
            for src in self.outgoing[port]['inside']:
                name1 = nodemap[src['node']] + ('_'+escape_port(src['port']) if 'port' in src else '')
                name2 = nodemap[self]+'_'+escape_port(port)
                lines.append(indent+'  '+name1+' -> '+name2+' [color=blue];')
        
        # tail
        lines.append(indent+'}')
    
    def store_dotfile (self, filename):
        lines = []
        counter = [0]
        nodemap = {}
        
        lines.append('digraph G {')
        lines.append('  compound=true;')
        self.as_dot(lines, nodemap, counter, indent='  ')
        lines.append('}')
        
        with open(filename, 'w') as fo:
            fo.writelines(map(lambda line: line+'\n', lines))

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
        
        if edgelist != None: edgelist.append(self)
    
    def primitive_src (self): return self.src_port == None
    def primitive_dst (self): return self.dst_port == None
    def complex_src (self): return not self.primitive_src()
    def complex_dst (self): return not self.primitive_dst()




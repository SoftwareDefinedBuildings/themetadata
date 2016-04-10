from abc import abstractmethod
import networkx as nx

# TODO: Redo ports so that port-to-port connections become possible

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
    def get_outgoing (self): return self.outgoing

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
    
    def get_nodes (self, nodelist=[], processed=[]):
        # guard: don't loop
        if self in processed: return
        processed.append(self)
        
        print(len(self.nodes))
        for node in self.nodes:
            if not node in processed:
                print('  '+str(type(node)))
                if type(node)==ComplexNode:
                    print('    recurse!')
                    node.get_nodes(nodelist, processed)
                nodelist.append(node)
                processed.append(node)
        print('--')
        return nodelist
    
    def find_dsts (self, port, dsts=[], nodelist=[]):
        print('complex node find dsts')
        # TODO: add a nodeportlist?
#        # new or processed node?
#        if self in nodelist:
#            return dsts
#        else:
#            nodelist.append(self)
        
        edges = self.incoming[port]['inside'] if port in self.incoming else self.outgoing[port]['outside']
        print('edges='+str(edges))
        for edge_dict in edges:
            node = edge_dict['node']
            if 'port' in edge_dict:
                node.find_dsts(edge_dict['port'], dsts, nodelist)
            else:
                nodelist.append(node)
                dsts.append(node)
        
        return dsts
    
    def export_nx (self):
        g = nx.DiGraph()
        counter = [0]
        nodemap = {}
        
        nodes = self.get_nodes()
        
        # add nodes
        for node in nodes:
            if type(node)==PrimitiveNode:
                nodemap[node] = 'node'+str(counter[0])
                counter[0] += 1
                g.add_node(nodemap[node], attr_dict=node.attrs)
        
        # add edges
        for node in nodes:
            print('node: '+str(node)+' ('+node.attrs['name']+')')
            if type(node)==PrimitiveNode:
                print('  primitive')
                edges = node.get_outgoing()
                for edge in edges:
                    print('  edge: '+str(edge))
                    if edge.primitive_dst():
                        print('    primitive dst='+str(edge.dst.attrs['name']))
                        g.add_edge(nodemap[node],nodemap[edge.dst])
                    else:
                        print('    complex dst='+str(edge.dst.attrs['name']))
                        dsts = edge.find_dsts()
                        for dst in dsts:
                            g.add_edge(nodemap[node],nodemap[dst])
            else:
                for port in node.outgoing:
                    dsts = []
                    for edge in node.outgoing[port]['outside']:
                        edge.find_dsts(dsts)
                    
                    print(dsts)
                    for edgedict in node.outgoing[port]['inside']:
                        for dst in dsts:
                            g.add_edge(nodemap[edgedict['node']],nodemap[dst])
        
        return g

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
    
    def find_dsts (self, dsts=[], nodelist=[]):
        # new or processed node?
        if self.dst in nodelist:
            return dsts
        
        if self.primitive_dst():
            nodelist.append(self.dst)
            dsts.append(self.dst)
        else:
            self.dst.find_dsts(self.dst_port, dsts, nodelist)
        
        return dsts


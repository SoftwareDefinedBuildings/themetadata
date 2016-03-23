The Metadata
============

This is the metadata. There are many like it but this one is ours.

## Goals

1. The metadata structure should support incremental construction. We may not
   know the full details of every building component when we begin, but we
   should not need to have a *complete* picture before we can start reasoning
   about the building's structure.
2. The eventual metadata structure should have a set of principled layers.
   Attempting to account for all possible use cases can introduce a lot of
   complexity, which makes it harder to understand and use the structure. With
   clear separation of concern between layers, "higher" layers can implement
   more specialized logic needed by fewer applications.

## Layered Approach

No one metadata structure can accomplish everything. Our approach here is to
implement a "root" structure that identifies the set of equipment and
infrastructure, relationships and connections between them, and logical
groupings of these elements. This solves the immediate problem of how to
programmatically reason about the structure of a building and what "things" are
inside it.

Once this layer is sufficiently developed, we can implement 'views' over it.
These views can introduce logic attached to elements or relationships in the
core representation. This is a driving principle for the development of this
initial layer: it should capture what things are there and how these things are
connected.  Responsibility for any additional information should probably be
relegated to a higher level.

## Basic Structure

Metadata is a directed graph. Nodes represent logical and physical components,
and edges represent the relationships between them.

### Node

A node has several components.

**Unique Identifier**: this serves as a pointer for overlays. For example, we may
have an object-oriented overlay that attaches methods to each node. Each object
instance could use a uuid to point into the base graph to traverse and find related
objects.

**Set of key-value pairs**: these describe the node ("metadata for your metadata")
and may include:
* a type or class?
* owner
* time installed
* manufacturer/model
* etc etc

**Set of in/out "ports"**: These capture the kinds of inputs a node accepts and
the kinds of outputs a node emits. An example would be an air handler unit,
which has "inputs" of outside air and return air, and "outputs" of exhaust air
and supply air. A port is referenced by a name. In-degree edges should be attached
to input ports and out-degree edges should be attached to output ports.

**Directed edges**: Edges are directed, and can have one of a set number of
types.  Types describe the nature of the relationship between the two node
endpoints. Types should be (mostly) orthogonal, that is, it should be clear to
a user which relationship should exist between two nodes.

The current array of edges types is as follows. For any relationship `<rel>`,
the nature of the edge is `X <rel> Y := X -> Y`.
* `Feeds`: some physical medium flows from X to Y
* `Has a`: don't need this?
* `Contains`: the node Y is a component *within* component X.

For controllers:
* `Controls`: if X is a controller, then Y is some entity that it acts on behalf of, e.g.
  a PID loop might have a "controls" relationship with an HVAC zone, which would "contain"
  a set of rooms.
* `Input`: X is some node that provides input to a controller Y, for example a temperature
  sensor and a temperature setpoint are both inputs to a temperature controller
* `Output`: X is some node whose state is the output of a controller, for example the
  damper position might be the output of an airflow controller.

**Internal graph**: A key goal of this metadata structure is supporting
incremental construction.  A part of this is how to deal with larger, more
complex components such as an air handling unit, which probably contains
connections to heating and/or cooling loops, several fans and dampers and
sensors. We may not know the construction of the airhandling unit, but we *do*
know that it supplies air to some array of variable air volume boxes (VAVs).
With a hierarchical graph, we can connect an Air Handling Unit node with a
"feeds" relationship on the "supply air" output port to a set of VAV nodes.

An internal graph consists of nodes and directed edges just like the "top
level" graph with the addition that nodes at the "edges" of the internal graph
should be connected to the named input/output ports of the encapsulating node.
Nodes in an internal graph are the endpoint of  "contains" edges with the encapsulating node.
An example will make this clear.

Answers the question: is the building metadata graph flat or hierarchical? Hierarchical.

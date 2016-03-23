The Metadata
============

This is the metadata. There are many like it but this one is ours.

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

**Internal graph**: 

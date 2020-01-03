"""
Graph save-load interface.

Ref 1: https://github.com/hadim/pygraphml/blob/master/pygraphml/graphml_parser.py
"""

import codecs
import inspect
import pickle
import warnings
from xml.etree.ElementTree import Element, ElementTree, parse, Comment


GRAPHML_TYPES = {bool: "bool", "bool": bool,
                 int: "int", "int": int,
                 float: "double", "long": float, "float": float, "double": float,
                 str: "string", "string": str,
                 "--iglsynth.pickled--": str}

NS_GRAPHML = "http://graphml.graphdrawing.org/xmlns"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
SCHEMA_LOCATION = 'http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd'
XML_HEADER = {'xmlns': NS_GRAPHML, 'xmlns:xsi': NS_XSI, 'xsi:schemaLocation': SCHEMA_LOCATION}
XML_IGLSYNTH = "This file is automatically generated by IGLSynth python library."


class GraphMLParser:
    """
    GraphML Parser for IGLSynth :class:`Graph` objects.
    """
    NS_GRAPHML = "http://graphml.graphdrawing.org/xmlns"
    NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
    SCHEMA_LOCATION = 'http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd'
    XML_HEADER = {'xmlns': NS_GRAPHML, 'xmlns:xsi': NS_XSI, 'xsi:schemaLocation': SCHEMA_LOCATION}

    def __init__(self, graph):
        self._graph = graph
        self.xml = Element("graphml", self.XML_HEADER)

    def indent(self, elem, level=0):
        # in-place prettyprint formatter
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def add_graph_properties(self):
        # Add name of graph class
        xml_data = Element("data", key="classname")
        xml_data.text = str(self._graph.__class__)
        self.xml.append(xml_data)

        # Gather user-defined attributes of graph
        user_attr = [key for key in self._graph.__dict__.keys() if not key.startswith("__")]

        # Add all graph attributes
        for key in user_attr:
            # Do not save default properties of base class Graph.
            if key in ['_edges', '_vertex_edge_map', 'edges', 'vertices', 'num_edges', 'num_vertices']:
                continue

            # Add graph attributes to graphml
            try:
                # Get value of user-attribute
                value = eval(f"self._graph.{key}")

                # Create xml element and add the key-value pair
                xml_data = Element("data", key=key)
                xml_data.text = str(value)
                self.xml.append(xml_data)

            except NotImplementedError:
                continue

    def add_node(self, xml_graph, v):
        xml_graph_node = Element("node", id=str(v.name))
        user_attr = [key for key in dir(v) if not key.startswith("__")]

        for key in user_attr:
            # Add graph attributes to graphml
            try:
                # Check if key is a property
                if key in dir(type(v)):
                    if isinstance(eval(f"type(v).{key}"), property):
                        continue

                # Get value of user-attribute
                value = eval(f"v.{key}")

                # Create xml element and add the key-value pair
                xml_graph_node_data = Element("data", key=key)
                xml_graph_node_data.text = str(value)
                xml_graph_node.append(xml_graph_node_data)

            except NotImplementedError:
                continue

        xml_graph.append(xml_graph_node)

    def add_edge(self, xml_graph, e):
        xml_graph_edge = Element("edge", id=str(e.name))
        user_attr = [key for key in dir(e) if not key.startswith("__")]

        for key in user_attr:
            # Add graph attributes to graphml
            try:
                # Check if key is a property
                if key in dir(type(e)):
                    if isinstance(eval(f"type(e).{key}"), property):
                        continue

                # Get value of user-attribute
                value = eval(f"e.{key}")

                # Create xml element and add the key-value pair
                xml_graph_edge_data = Element("data", key=key)
                xml_graph_edge_data.text = str(value)
                xml_graph_edge.append(xml_graph_edge_data)

            except NotImplementedError:
                continue

        xml_graph.append(xml_graph_edge)

    def write(self, fname):
        """
        Generate GraphML file for given graph object.
        """
        # xml = Element("graphml", self.XML_HEADER)

        # In IGLSynth we deal with only directed graphs
        xml_graph = Element("graph", {'edgedefault': 'directed',
                                      'parse.nodes': str(self._graph.num_vertices),
                                      'parse.edges': str(self._graph.num_edges)})
        self.xml.append(xml_graph)

        # Add graph class properties/attributes
        self.add_graph_properties()

        # Add nodes of graph
        for v in self._graph.vertices:
            self.add_node(xml_graph=xml_graph, v=v)

        # Add edges of graph
        for e in self._graph.edges:
            self.add_edge(xml_graph=xml_graph, e=e)

        # Generate document
        self.indent(self.xml)
        document = ElementTree(self.xml)
        document.write(fname, encoding='utf-8', xml_declaration=True)

    def read(self, fname):
        """Read a GraphML document. Produces IGLSynth graph objects."""

        # Parse the file into XML element tree
        tree = parse(fname)
        graphml = tree.getroot()

        # Set graph properties
        for data in graphml.findall("{%s}data" % self.NS_GRAPHML):
            key = data.attrib['key']
            value = data.text

            if key == 'vtype' and str(self._graph.vtype) != value:
                warnings.warn("GraphML.Graph.vtype and graph.vtype don't match.")

            if key == 'etype' and str(self._graph.etype) != value:
                warnings.warn("GraphML.Graph.etype and graph.etype don't match.")


class GraphMLWriter(object):
    """
    Writes given graph object as a graphml file.

    Format:
        <graphml ... >
            <!-- IGLSYNTH AUTO-GENERATED COMMENT -->

            <key id="varname" for="node/edge" attr.name="varname" attr.type="iglsynth-graphml-types">
                <default> PICKLE_SERIALIZED_VALUE </default>
            </key>
            ..

            <data key=".."> PICKLE_SERIALIZED_VALUE </data>
            ..

            <graph>
                <node id="..">
                    <data key=".."> PICKLE_SERIALIZED_VALUE </data>
                    ..
                </node>

                <edge id="..">
                    <data key=".."> PICKLE_SERIALIZED_VALUE </data>
                    ..
                </edge>
            </graph>
        <graphml>

    iglsynth-graphml-types include special string: "--iglsynth.pickled--" which
    indicates that the value is a pickled value.

    :param graph: (:class:`Graph`) Graph to be saved in graphml format.
    """
    def __init__(self, graph):
        self._graph = graph
        self._xml = Element("graphml", XML_HEADER)
        self._xml_graph = Element("graph", {'edgedefault': 'directed',
                                            'parse.nodes': str(self._graph.num_vertices),
                                            'parse.edges': str(self._graph.num_edges)})
        self._xml.append(self._xml_graph)

    def _add_vprop_keys(self, props):
        pass

    def _add_eprop_keys(self, props):
        pass

    def _add_gprop_keys(self, props):

        # List of elements to store XML elements
        elem_buffer = []

        # Add special properties: name of graph class, vertex class, edge class
        cls_graph_elem = Element("data", key="graph_class_name")
        cls_graph_elem.text = self._get_graph_class_name()
        elem_buffer.append(cls_graph_elem)

        cls_vertex_elem = Element("data", key="vertex_class_name")
        cls_vertex_elem.text = self._get_graph_vertex_class_name()
        elem_buffer.append(cls_vertex_elem)

        cls_edge_elem = Element("data", key="edge_class_name")
        cls_edge_elem.text = self._get_graph_edge_class_name()
        elem_buffer.append(cls_edge_elem)

        for p_name, p_type in props:
            try:
                # Create a new element
                new_key = Element("data", key=f"{p_name}")

                # Pickle the value
                value = pickle.dumps(eval(f"self._graph.{p_name}", {"self": self}))

                # Convert picked byte object to string
                value = codecs.encode(value, "base64").decode()

                # Assign value to element
                new_key.text = value

                # Append element to list of new elements to add to GraphML file
                elem_buffer.append(new_key)

            except (NotImplementedError, ):
                continue

        for elem in elem_buffer:
            self._xml_graph.append(elem)

    def _get_graph_class_name(self):
        return self._graph.__class__.__qualname__

    def _get_graph_vertex_class_name(self):
        return self._graph.vtype.__qualname__

    def _get_graph_edge_class_name(self):
        return self._graph.etype.__qualname__

    def _get_vertex_properties(self):
        pass

    def _get_edge_properties(self):
        pass

    def _get_graph_properties(self):
        # Get all members of the graph
        obj_members = dir(self._graph)
        cls_members = dir(self._graph.__class__)

        # Construct list of useful graph members
        gprops = list()
        local_variables = {"self": self, "inspect": inspect}
        for m in obj_members:
            try:
                # Remove if member is in-built python variable
                if m.startswith("__"):
                    continue

                # Remove if member is internal graph representation variable
                if m in ["_edges", "_vertex_edge_map"]:
                    continue

                # Remove if member is a abstract object, a class, a method, or a function
                if eval(f"inspect.isabstract(self._graph.{m})", local_variables):
                    continue

                if eval(f"inspect.ismethod(self._graph.{m})", local_variables):
                    continue

                if eval(f"inspect.isfunction(self._graph.{m})", local_variables):
                    continue

                if eval(f"inspect.isclass(self._graph.{m})", local_variables):
                    continue

                # Remove if member is a property
                #   Note: Properties are associated with class, not the object.
                if m in cls_members and eval(f"isinstance(self._graph.__class__.{m}, property)", local_variables):
                    continue

                # If all checks are passed, then member is a graph internal property
                gprops.append((m, eval(f"type(self._graph.{m})", local_variables)))

            except (NotImplementedError, AttributeError):
                continue

        return gprops

    def _indent(self, elem, level=0):
        """ Adopted from NetworkX graphml parsing library. """
        # in-place prettyprint formatter
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def write(self, fname):

        # Identify vertex properties and their types
        vprops = self._get_vertex_properties()

        # Identify edge properties and their types
        eprops = self._get_edge_properties()

        # Identify graph properties and their types
        gprops = self._get_graph_properties()

        # Write vertex and edge property information
        self._add_vprop_keys(vprops)
        self._add_eprop_keys(eprops)
        self._add_gprop_keys(gprops)

        # Add comment that this file is generated by IGLSynth
        comment = Comment(XML_IGLSYNTH)
        self._xml.append(comment)

        # Generate GraphML file
        self._indent(self._xml)
        document = ElementTree(self._xml)
        document.write(fname, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    from iglsynth.util.graph import *

    g = Graph()

    v0 = g.Vertex()
    v1 = g.Vertex()
    g.add_vertices([v0, v1])

    writer = GraphMLWriter(graph=g)
    writer.write(fname="graph1.graphml")

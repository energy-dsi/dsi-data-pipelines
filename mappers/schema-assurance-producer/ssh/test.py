

import os

from rdflib import Graph

from dsi_schema_assurance import SchemaCertifier


ontology_path = os.path.join(os.getcwd(), 'validation_files', 'ontology.rdf')
ontology_graph = Graph()
ontology_graph.parse(ontology_path, format="xml")

shacl_path = os.path.join(os.getcwd(), 'validation_files', 'shacl.ttl')
shacl_graph = Graph()
shacl_graph.parse(shacl_path, format="turtle")


data_path = '/Users/joao.nisa/Desktop/OneDrive_1_18-02-2025-2/SSH.xml'
data_graph = Graph()
data_graph.parse(data_path, format="xml")

certifier = SchemaCertifier(
    data_graph = data_graph,
    shacl_graph = shacl_graph,
    ont_graph = ontology_graph,
    inference_type = 'both'
).run()

breakpoint()
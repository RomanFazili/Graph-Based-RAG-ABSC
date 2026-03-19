from data_set_ontology import DataSetOntology
from dotenv import load_dotenv
import os
from rdflib import Graph


class OntologyRetriever:

    def __init__(self, data_set_ontology: DataSetOntology):
        self.data_set_ontology: DataSetOntology = data_set_ontology

    def find_all_reachable_nodes(self, subject_or_object: str) -> Graph:
        """
        Execute the given SPARQL 1.1 query (with property paths) using rdflib
        and return the resulting RDF graph as an rdflib.Graph.
        """
        g: Graph = self.data_set_ontology.get_rdflib_graph()

        sparql_query = f"""
        CONSTRUCT {{
          ?s ?p ?o .
        }}
        WHERE {{
          <{subject_or_object}> (^<>|!<>)* ?node .
          
          {{ ?node ?p ?o . BIND(?node AS ?s) }}
          UNION
          {{ ?s ?p ?node . BIND(?node AS ?o) }}
        }}
        """

        qres = g.query(sparql_query)
        return qres.graph


if __name__ == "__main__":
    load_dotenv()
    file_path = os.getenv("PATH_TO_RESTAURANT_ONTOLOGY")
    data_set_ontology = DataSetOntology(file_path)
    ontology_retriever = OntologyRetriever(data_set_ontology)

    start_uri = "http://www.kimschouten.com/sentiment/restaurant#Mention"
    reachable_graph = ontology_retriever.find_all_reachable_nodes(start_uri)

    # Serialize result as proper RDF/XML
    reachable_graph.serialize(destination="reachable_subgraph.owl", format="xml")
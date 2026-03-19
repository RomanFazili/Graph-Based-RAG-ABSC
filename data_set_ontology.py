import os
from dotenv import load_dotenv
from owlready2 import Ontology, get_ontology
from rdflib import Graph


class DataSetOntology:

    def __init__(self, file_path: str):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist")
        if not file_path.endswith(".owl"):
            raise ValueError(f"The file {file_path} is not an OWL file")

        self.file_path = file_path

        self.ontology: Ontology = get_ontology(f"file://{os.path.abspath(self.file_path)}").load()
        self._graph: Graph | None = None

    def get_rdflib_graph(self) -> Graph:
        """
        Load the ontology file into an rdflib Graph, so we can execute
        SPARQL 1.1 queries.
        """
        if self._graph is None:
            g = Graph()
            g.parse(self.file_path)
            self._graph = g
        return self._graph


if __name__ == "__main__":
    load_dotenv()
    file_path = os.getenv("PATH_TO_RESTAURANT_ONTOLOGY")

    data_set_ontology = DataSetOntology(file_path)
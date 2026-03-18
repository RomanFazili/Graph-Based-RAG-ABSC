from data_set_ontology import DataSetOntology
from dotenv import load_dotenv
import os

class OntologyRetriever:

    def __init__(self, data_set_ontology: DataSetOntology):
        self.data_set_ontology: DataSetOntology = data_set_ontology

    def find_all_reachable_nodes(self, subject_or_object: str):

        sparql_query = """
            SELECT ?s ?p ?o
            WHERE {
            { <http://www.kimschouten.com/sentiment/restaurant#AmbienceMention> ?p ?o .
                BIND(<http://www.kimschouten.com/sentiment/restaurant#AmbienceMention> AS ?s)
            }
            UNION
            { ?s ?p <http://www.kimschouten.com/sentiment/restaurant#AmbienceMention> .
                BIND(<http://www.kimschouten.com/sentiment/restaurant#AmbienceMention> AS ?o)
            }
            }
            """

        # Delegate to the dataset's SPARQL runner so we use the correct
        # Owlready2 world.sparql API.
        return self.data_set_ontology.run_sparql_query(sparql_query)

if __name__ == "__main__":
    load_dotenv()
    file_path = os.getenv("PATH_TO_RESTAURANT_ONTOLOGY")
    data_set_ontology = DataSetOntology(file_path)
    ontology_retriever = OntologyRetriever(data_set_ontology)
    all_reachable_nodes = ontology_retriever.find_all_reachable_nodes("http://www.kimschouten.com/sentiment/restaurant#AmbienceMention")
    print(all_reachable_nodes)


    for node in all_reachable_nodes:
        print(node[0], node[1], node[2])

        print(type(node[0]), type(node[1]), type(node[2]))
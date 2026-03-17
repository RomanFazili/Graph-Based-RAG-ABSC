import xml.etree.ElementTree as ET
import os
from enum import StrEnum

class Polarity(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class DataImplementation:

    def __init__(self, file_path: str):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist")
        if not file_path.endswith(".xml"):
            raise ValueError(f"The file {file_path} is not an XML file")

        self.file_path = file_path
        self.tree: ET.ElementTree = ET.parse(self.file_path)

    @property
    def root(self) -> ET.Element:
        return self.tree.getroot()

    @property
    def all_sentences(self) -> list[str]:
        return [sentence.find('text').text for sentence in self.root.findall('.//sentence')]

    def tokenize(self, input: str) -> list[str]:
        return input.lower().split(' ')

    def polarity_frequencies(self):
        raise NotImplementedError("Polarity frequencies is not implemented")

    def BM25_demonstration_selection(self, query_sentence: str, top_k: int):
        raise NotImplementedError("BM25 demonstration selection is not implemented")

    def SimCSE_demonstration_selection(self, query_sentence: str, top_k: int):
        raise NotImplementedError("SimCSE demonstration selection is not implemented")

if __name__ == "__main__":
    file_path = input("Enter the path to the XML file: ")
    data_implementation = DataImplementation()
    print(data_implementation.polarity_frequencies())
    print(data_implementation.BM25_demonstration_selection("The food was good", 3))
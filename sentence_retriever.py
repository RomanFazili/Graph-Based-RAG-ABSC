from data_implemenation import DataSet



class SentenceRetriever:

    def __init__(self, data_set: DataSet):
        self.data_set = data_set

    def BM25_demonstration_selection(self, query_sentence: str, top_k: int):
        raise NotImplementedError("BM25 demonstration selection is not implemented")

    def SimCSE_demonstration_selection(self, query_sentence: str, top_k: int):
        raise NotImplementedError("SimCSE demonstration selection is not implemented")



if __name__ == "__main__":
    file_path = input("Enter the path to the XML file: ")
    data_set = DataSet(file_path)
    sentence_retriever = SentenceRetriever(data_set)
    print(sentence_retriever.BM25_demonstration_selection("The food was good", 3))
    print(sentence_retriever.SimCSE_demonstration_selection("The food was good", 3))
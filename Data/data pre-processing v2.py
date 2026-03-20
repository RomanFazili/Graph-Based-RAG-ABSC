import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

def convert_semeval14_to_15_16_format(semeval14_filepath: str, output_path: str):

    tree: ET.ElementTree = ET.parse(semeval14_filepath)
    root: ET.Element = tree.getroot()

    # Create a new root and subroot elements for the new structure
    new_root: ET.Element = ET.Element("Reviews")
    review: ET.Element = ET.SubElement(new_root, "Review")
    sentences: ET.Element = ET.SubElement(review, "sentences")
    
    for sentence in root.findall("sentence"):
        sentence_id = sentence.get("id")
        text = sentence.find("text").text

        new_sentence = ET.SubElement(sentences, "sentence", id=sentence_id)
        ET.SubElement(new_sentence, "text").text = text
        
        opinions = ET.SubElement(new_sentence, "Opinions")

        # Convert <aspectTerms> into <Opinions>
        aspect_terms = sentence.find("aspectTerms")
        if aspect_terms is not None:
            # Case 1: aspectTerm is present
            for aspect in aspect_terms.findall("aspectTerm"):
                target = aspect.get("term")
                polarity = aspect.get("polarity")
                from_idx = aspect.get("from")
                to_idx = aspect.get("to")
                ET.SubElement(opinions, "Opinion", target=target, category="", polarity=polarity, from_=from_idx, to=to_idx)
        else:
            # Case 2: no aspectTerm is present, set target = NULL
            ET.SubElement(opinions, "Opinion", target="NULL")

    # Write the converted XML to the output file
    tree = ET.ElementTree(new_root)
    ET.indent(tree, space="    ", level=0)
    tree.write(
        file_or_filename=output_path,
        encoding="utf-8",
        xml_declaration=True,
        method="xml"
    )
    print(f"Converted SemEval14 dataset saved to: {output_path}")

# Definition to delete the implict aspect from the dataset (only works for 2015/2016 XML structure!)
def delete_implicit_aspects_and_conflicting_polarities(input_path: str, output_path: str):
    """
    Deletes the implicit aspects (target = null) from the dataset.
    Deletes any opinions with a conflicting polarity (polarity = conflict).
    Deletes any sentences without any non-null opinions.
    """

    tree: ET.ElementTree = ET.parse(input_path)
    root: ET.Element = tree.getroot()

    amount_null_target_opinions: int = 0
    amount_conflicting_polarities: int = 0
    amount_sentences_removed: int = 0

    #Iterature over all reviews and sentences
    for review in root.findall('.//Review'):
        sentences: ET.Element = review.find('sentences')
            
        sentences_to_remove: list[ET.Element] = []
        
        for sentence in sentences.findall('sentence'):
            opinions_elem = sentence.find('Opinions')
            if opinions_elem is None:
                sentences_to_remove.append(sentence)
                continue
                
            # Remove all null target opinions
            for opinion in list(opinions_elem.findall('Opinion')):
                if opinion.get("target") == "NULL":
                    opinions_elem.remove(opinion)
                    amount_null_target_opinions += 1

            # Remove all conflicting polarities
            for opinion in list(opinions_elem.findall('Opinion')):
                if opinion.get("polarity") == "conflict":
                    opinions_elem.remove(opinion)
                    amount_conflicting_polarities += 1

            # Remove any sentence without any opinions
            if not opinions_elem.findall("Opinion"):
                sentences_to_remove.append(sentence)

        # Remove sentences to remove
        for sentence in sentences_to_remove:
            sentences.remove(sentence)

        amount_sentences_removed += len(sentences_to_remove)

    # Write the modified XML to the output file
    ET.indent(tree, space="    ", level=0)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Dataset with implicit aspects removed saved to: {output_path}")
    print(f"Amount of null target opinions: {amount_null_target_opinions}")
    print(f"Amount of conflicting polarities: {amount_conflicting_polarities}")
    print(f"Amount of sentences without opinions: {amount_sentences_removed}")

# Definition to remove intersections between train and test data from the train data
def remove_intersections(training_input_path: str, test_input_path: str, training_output_path: str):
    """
    Removes any sentences from the training data that are also present in the test data.
    """

    def text_from_sentence(sentence: ET.Element) -> str:
        return sentence.find('text').text.strip()

    print(training_input_path)
    print(test_input_path)


    test_tree: ET.ElementTree = ET.parse(test_input_path)
    test_root: ET.Element = test_tree.getroot()
    test_sentences: set[str] = {text_from_sentence(sentence) for sentence in test_root.findall('.//sentence')}

    training_tree: ET.ElementTree = ET.parse(training_input_path)
    training_root: ET.Element = training_tree.getroot()

    amount_sentences_removed: int = 0
    
    for review in training_root.findall('.//Review'):
        sentences: ET.Element = review.find('sentences')
            
        sentences_to_remove: list[ET.Element] = []
        for sentence in sentences.findall('sentence'):
            if text_from_sentence(sentence) in test_sentences:
                sentences_to_remove.append(sentence)

        for sentence in sentences_to_remove:
            sentences.remove(sentence)

        amount_sentences_removed += len(sentences_to_remove)

    ET.indent(training_tree, space="  ", level=0)
    training_tree.write(training_output_path, encoding="utf-8", xml_declaration=True)
    print(f"Training Dataset with intersections removed saved to: {training_output_path}")
    print(f"Amount of sentences removed: {amount_sentences_removed}")


# Convert the SemEval14 dataset to the SemEval15/16 format
semeval14_input_output_paths: list[tuple[str, str]] = [
    (os.getenv("PATH_TO_RAW_SEMEVAL_14_RESTAURANTS_TRAIN_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TRAIN_DATA")),
    (os.getenv("PATH_TO_RAW_SEMEVAL_14_RESTAURANTS_TEST_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TEST_DATA"))
]

for semeval14_input_path, semeval14_output_path in semeval14_input_output_paths:
    convert_semeval14_to_15_16_format(
        semeval14_filepath=semeval14_input_path,
        output_path=semeval14_output_path
    )

# Delete the implicit aspects from all datasets
all_input_output_paths: list[tuple[str, str]] = [
    (os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TRAIN_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TRAIN_DATA")),
    (os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TEST_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TEST_DATA")),
    (os.getenv("PATH_TO_RAW_SEMEVAL_15_RESTAURANTS_TRAIN_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_15_RESTAURANTS_TRAIN_DATA")),
    (os.getenv("PATH_TO_RAW_SEMEVAL_15_RESTAURANTS_TEST_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_15_RESTAURANTS_TEST_DATA")),
    (os.getenv("PATH_TO_RAW_SEMEVAL_16_RESTAURANTS_TRAIN_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_16_RESTAURANTS_TRAIN_DATA")),
    (os.getenv("PATH_TO_RAW_SEMEVAL_16_RESTAURANTS_TEST_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_16_RESTAURANTS_TEST_DATA"))
]

for input_path, output_path in all_input_output_paths:
    delete_implicit_aspects_and_conflicting_polarities(
        input_path=input_path,
        output_path=output_path
    )

# Remove the intersections between the train and test data from the train data
all_input_output_paths_train: list[tuple[str, str, str]] = [
    (os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TRAIN_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TEST_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_14_RESTAURANTS_TRAIN_DATA")),
    (os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_15_RESTAURANTS_TRAIN_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_15_RESTAURANTS_TEST_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_15_RESTAURANTS_TRAIN_DATA")),
    (os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_16_RESTAURANTS_TRAIN_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_16_RESTAURANTS_TEST_DATA"), os.getenv("PATH_TO_PREPROCESSED_SEMEVAL_16_RESTAURANTS_TRAIN_DATA"))
]

for training_input_path, test_input_path, training_output_path in all_input_output_paths_train:
    remove_intersections(
        training_input_path=training_input_path,
        test_input_path=test_input_path,
        training_output_path=training_output_path
    )
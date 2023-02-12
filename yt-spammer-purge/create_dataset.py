import glob
import json

import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector


def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)

nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)


def get_label(label_str: str):
    return 0 if label_str == "False" else 1


def create_dataset(directory_path, dataset_path):
    dataset = []
    for filename in glob.iglob(f'{directory_path}*.json'):
        with open(filename, "r",encoding="utf8") as source:
            data = [json.loads(line) for line in source]
        
        for entry in data:
            dataset.append({"comment": entry["commentText"], "label": get_label(entry["isSpam"])})
            """doc = nlp(entry["commentText"])
            detect_language = doc._.language
            if detect_language["language"] == "en":
                dataset.append({"comment": entry["commentText"], "label": get_label(entry["isSpam"])})
            else:
                print(entry["commentText"], "\n")"""

    spomments = len([comment for comment in dataset if comment["label"]==1])
    legitimate = len([comment for comment in dataset if comment["label"]==0])
    print(f"Dataset with {len(dataset)} comments (spam: {spomments}, legitimate: {legitimate}) was created in {dataset_path}")

    with open(dataset_path, "a+", encoding="utf8") as file:
        file.truncate(0)
        file.seek(0)
        json.dump(dataset, file, indent=2)


if __name__=='__main__':
    directory = "logs/"
    dataset_file = "../dataset/dataset.json"
    create_dataset(directory, dataset_file)

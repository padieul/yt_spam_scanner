import csv
import glob
import json
import os
import pandas as pd



def get_label(label_str: str):
    return 0 if label_str == "False" else 1


def create_dataset_csv(directory_path, dataset_path, header=["CONTENT","CLASS"]):
    """Create dataset from given json files and store it in csv file"""
    dataset = []
    for filename in glob.iglob(f'{directory_path}*.json'):
        with open(filename, "r",encoding="utf8") as source:
            data = [json.loads(line) for line in source]

        for entry in data:
            dataset.append([entry["commentText"].strip().rstrip(), get_label(entry["isSpam"])])
            if get_label(entry["isSpam"])==1:
                # resample
                for i in range(0,9):
                    dataset.append([entry["commentText"].strip().rstrip(), get_label(entry["isSpam"])])

    spomments = len([comment for comment in dataset if comment[1]==1])
    legitimate = len([comment for comment in dataset if comment[1]==0])
    print(f"Dataset with {len(dataset)} comments (spam: {spomments}, legitimate: {legitimate}) was created in {dataset_path}")

    with open(dataset_path, "a+",encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(dataset)


def filter_comment_text(text):
    #filtered = text.encode('utf-8').strip()
    filtered = text.replace("\n", "").replace("\"\"", "").replace("\"", "")
    filtered = filtered.replace("\"", "")
    filtered = filtered.replace("\r", "")
    return filtered

def create_dataset_json(directory_path, dataset_path):
    dataset = []
    for filename in glob.iglob(f'{directory_path}*.json'):
        with open(filename, "r",encoding="utf8") as source:
            data = [json.loads(line) for line in source]
        
        for entry in data:
            dataset.append({"comment": filter_comment_text(entry["commentText"]), "label": get_label(entry["isSpam"])})

    spomments = len([comment for comment in dataset if comment["label"]==1])
    legitimate = len([comment for comment in dataset if comment["label"]==0])
    print(f"Dataset with {len(dataset)} comments (spam: {spomments}, legitimate: {legitimate}) was created in {dataset_path}")

    with open(dataset_path, "a+", encoding="utf8") as file:
        file.truncate(0)
        file.seek(0)
        json.dump(dataset, file, indent=2)

def json_to_csv(filename, dataset_output_file):
    #COMMENT_ID,AUTHOR,DATE,CONTENT,CLASS
    df = pd.read_json(filename)
    df = df.rename(columns={"comment": "CONTENT", "label": "CLASS"})
    df = resample_spam(df)

    df.to_csv(dataset_output_file, index=False, encoding='utf-8-sig')
    
def resample_spam(data_f):
    spam_data_f = data_f.loc[data_f["CLASS"] == 1]
    spam_data_f_nine = pd.concat([spam_data_f]*9, ignore_index=True)
    data_f = pd.concat([spam_data_f_nine, data_f])
    return data_f


if __name__=='__main__':
    directory = "logs/"
    dataset_json = "../dataset/dataset.json"
    dataset_csv = "../dataset/dataset.csv"
    create_dataset_csv(directory, dataset_csv)
    #create_dataset_json(directory, dataset_json)
    #json_to_csv(dataset_json, dataset_csv)

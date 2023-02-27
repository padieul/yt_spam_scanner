import csv
import glob
import json

# paths
DIRECTORY_LOGS = "../yt-spammer-purge/logs/"
DATASET_CSV = "./dataset.csv"


def get_label(label_str: str):
    """Return 0 (legitimate) or 1 (spam)"""
    return 0 if label_str == "False" else 1

def filter_comment_text(text):
    """Clean/preprocess comment text"""
    filtered = text.replace("\n", "").replace("\"\"", "").replace("\"", "")
    filtered = filtered.replace("\"", "")
    filtered = filtered.replace("\r", "")
    return filtered

def create_dataset_csv(directory_path, dataset_path):
    """Create dataset from given json files and store it in csv file"""
    dataset = []
    for filename in glob.iglob(f'{directory_path}*.json'):
        with open(filename, "r",encoding="utf8") as source:
            data = [json.loads(line) for line in source]

        for entry in data:
            dataset.append([filter_comment_text(entry["commentText"].strip().rstrip()), get_label(entry["isSpam"])])
            if get_label(entry["isSpam"])==1:
                # resample
                for i in range(0,9):
                    dataset.append([filter_comment_text(entry["commentText"].strip().rstrip()), get_label(entry["isSpam"])])

    spomments = len([comment for comment in dataset if comment[1]==1])
    legitimate = len([comment for comment in dataset if comment[1]==0])
    print(f"Dataset with {len(dataset)} comments (spam: {spomments}, legitimate: {legitimate}) was created in {dataset_path}")

    with open(dataset_path, "a+",encoding="utf8") as file:
        header=["CONTENT","CLASS"]
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(dataset)

if __name__=='__main__':
    create_dataset_csv(DIRECTORY_LOGS, DATASET_CSV)

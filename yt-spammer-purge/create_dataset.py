import glob
import json

def create_dataset(directory_path, dataset_path):
    dataset = []
    for filename in glob.iglob(f'{directory_path}*.json'):
        with open(filename, "r",encoding="utf8") as source:
            data = [json.load(line) for line in source]
        
        for entry in data:
            dataset.extend({"comment": entry["commentText"], "label": int(entry["isSpam"])})

    with open(dataset_path, "a+", encoding="utf8") as file:
        file.truncate(0)
        file.seek(0)
        json.dump(dataset, file, indent=2)


if __name__=='__main__':
    directory = "logs/"
    dataset_file = "./dataset.json"
    create_dataset(directory, dataset_file)

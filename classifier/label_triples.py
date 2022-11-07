import argparse
from postgresAPI import PostgresAPI
import torch
from model.triple_classifier import TripleClassifier
from torch.utils import data
from transformers import AutoTokenizer
import json

class Dataset(data.Dataset):
    def __init__(self, dataset, tokenizer_name='distilbert-base-uncased-finetuned-sst-2-english'):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, use_fast=False)
        self.dataset = dataset
        self.dataset['meta'] = self.dataset['meta'].apply(lambda x: json.dumps(x))
        
        # self.df = pd.DataFrame([self.dataset['text'] + ": " + self.dataset['meta']]).T
        # self.df.columns = ['text']
        # self.df['label'] = self.dataset['label']
    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        text = self.dataset['text'][index]
        meta = json.loads(self.dataset['meta'][index])
        entity_type = meta.pop('entity_type')
        
        meta = json.dumps(list(meta.keys()))

        text = 'entity type: ' + entity_type + ' meta: ' + text + ' ' + meta

        token = self.tokenizer.encode_plus(text, truncation=True, max_length=512, padding="max_length", return_tensors="pt")
        token = {'text':token['input_ids']}
        return token        


def main(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    db = PostgresAPI(dbname=args.database, user=args.user, password=args.password, host=args.host, port=args.port)
    model = load_model(args.model_name, device)
    upper, lower = load_threasold(args.model_name)
    done = False
    samples = db.get_unlabeled_data("triple classification", args.batch_size)
    ids = set()
    for df in samples:
        dataset = Dataset(df)
        dataloader = data.DataLoader(dataset, batch_size=args.batch_size, shuffle=False)
        for batch in dataloader:
            label = model.predict(batch, upper, lower)
            for i, label in zip(df['id'], label):
                # check if id is already in ids
                if i not in ids:
                    ids.add(i)
                else:
                    print("id already in ids")
                if label == 1:
                    db.update_label(i, "Positive")
                elif label == 0:
                    db.update_label(i, "Negative")
            





def load_model(model_name, device):
    model = TripleClassifier(device, model_name=model_name)
    model.load("model/"+model_name+"_triple_classifier.pt")
    return model

def load_threasold(model_name):
    # read txt file in model folder
    threashold = open("model/"+model_name+"_threshold_triple_classifier.txt", "r").read().splitlines()
    upper = float(threashold[0])
    lower = float(threashold[1])
    return upper, lower




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=str, default="5432")
    parser.add_argument("--user", type=str, default="postgres")
    parser.add_argument("--password", type=str, default="postgres")
    parser.add_argument("--database", type=str, default="postgres")
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--batch_size", type=int, default=10)
    
    
    args = parser.parse_args()
    main(args)
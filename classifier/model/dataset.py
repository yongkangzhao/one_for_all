from torch.utils import data
import argparse
import pandas as pd
from transformers import AutoTokenizer
import json
# sampler with balanced distribution

class TripleDataset(data.Dataset):
    def __init__(self, dataset_path, tokenizer_name='distilbert-base-uncased-finetuned-sst-2-english'):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, use_fast=False)
        self.dataset = pd.read_csv(dataset_path)
        self.dataset = self.dataset.sample(frac=1).reset_index(drop=True)
        # self.df = pd.DataFrame([self.dataset['text'] + ": " + self.dataset['meta']]).T
        # self.df.columns = ['text']
        # self.df['label'] = self.dataset['label']
    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        text = self.dataset['text'][index]
        meta = json.loads(self.dataset['meta'][index])
        label = self.dataset['label'][index]

        entity_type = meta.pop('entity_type')
        meta = json.dumps(list(meta.keys()))

        text = 'entity type: ' + entity_type + ' meta: ' + text + ' ' + meta

        token = self.tokenizer.encode_plus(text, truncation=True, max_length=512, padding="max_length", return_tensors="pt")
        token = {'text':token['input_ids'], 'label': label}
        return token        


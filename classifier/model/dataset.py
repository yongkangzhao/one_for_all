from torch.utils import data
import argparse
import pandas as pd
from transformers import AutoTokenizer

# sampler with balanced distribution

class TripleDataset(data.Dataset):
    def __init__(self, dataset_path):
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased", use_fast=False)
        self.dataset = pd.read_csv(dataset_path)
        self.dataset = self.dataset.sample(frac=1).reset_index(drop=True)
        self.df = pd.DataFrame([self.dataset['entity_type'] +": "+ self.dataset['text'] + " meta: " + self.dataset['meta']]).T
        self.df.columns = ['text']
        self.df['label'] = self.dataset['label']
    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        token = self.tokenizer.encode_plus(list(self.df.iloc[index]['text']), truncation=True, max_length=512, padding="max_length", return_tensors="pt")
        token = {'text':token['input_ids'], 'label': self.df.iloc[index]['label']}
        return token        


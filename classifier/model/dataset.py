from torch.utils import data
import argparse
import pandas as pd

# sampler with balanced distribution

class TripleDataset(data.Dataset):
    def __init__(self, dataset_path):
        self.dataset = pd.read_csv(dataset_path)
        self.dataset = self.dataset.sample(frac=1).reset_index(drop=True)
        self.df = pd.DataFrame([self.dataset['entity_type'] +": "+ self.dataset['text'] + " [SEP] meta: " + self.dataset['meta']]).T
        self.df.columns = ['text']
        self.df['label'] = self.dataset['label']
    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        return self.df.iloc[index]


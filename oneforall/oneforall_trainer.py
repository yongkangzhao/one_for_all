from __future__ import print_function
from typing import List, Tuple
from tqdm import tqdm
import torch

from datasets import load_dataset
from transformers import PreTrainedTokenizer, T5ForConditionalGeneration, T5Tokenizer, AdamW, set_seed
from torch.utils.data import DataLoader
import argparse

from dataset import Dataset, DatasetMap 

import pandas as pd


def train(model: T5ForConditionalGeneration, tokenizer: PreTrainedTokenizer, optimizer: AdamW, train_set: Dataset, validation_set: Dataset, num_train_epochs: int, device: str, batch_size: int, max_input_length: int = 512):
    
    """_summary_

    Args:
        model (T5ForConditionalGeneration): _description_
        tokenizer (PreTrainedTokenizer): _description_
        optimizer (AdamW): _description_
        train_set (Dataset): _description_
        validation_set (Dataset): _description_
        num_train_epochs (int): _description_
        device (str): _description_
        batch_size (int): _description_
    """
    my_trainset_dataloader = DataLoader(train_set, batch_size=args.batch_size,
                                        num_workers=args.workers, collate_fn=lambda data: train_set.pack_minibatch(data))
    my_validation_dataloader = DataLoader(validation_set, batch_size=args.batch_size,
                                          num_workers=args.workers, collate_fn=lambda data: validation_set.pack_minibatch(data))

    # set training mode on the model
    model.train()

    # model to device
    model.to(device)

    f1_old: int = 0
    for epoch in range(num_train_epochs):
        epoch_train_loss = 0.
        for contexts,questions,answers in tqdm(my_trainset_dataloader):
            optimizer.zero_grad()

            inputs = list(map(lambda tuple: f"question:{tuple[0]}  context:{tuple[1]}", zip(questions,contexts)))
            encoded_inputs = tokenizer(
                                    inputs,
                                    padding="longest",
                                    max_length=max_input_length,
                                    truncation=True,
                                    return_tensors="pt",
                                )
            encoded_targets = tokenizer(
                                    answers,
                                    padding="longest",
                                    max_length=max_input_length,
                                    truncation=True,
                                    return_tensors="pt",
                                )

            input_ids, attention_mask = encoded_inputs.input_ids, encoded_inputs.attention_mask
            encoded_targets = encoded_targets.input_ids

            # replace padding target token id's of the labels by -100, crossEntropy skip target label == -100
            encoded_targets[encoded_targets == tokenizer.pad_token_id] = -100

            input_ids = input_ids.to(device)
            encoded_targets = encoded_targets.to(device)
            attention_mask = attention_mask.to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=encoded_targets)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            epoch_train_loss += loss.item() * batch_size
        print(f"epoch={epoch + 1}/{num_train_epochs}")
        print(f"\t Train loss = {epoch_train_loss/len(train_set):.4f}")

        model.eval()
        with torch.no_grad():
            model_predictions_encoded = []
            target_encoded = []
            for contexts, questions, answers in tqdm(my_validation_dataloader):
                inputs = list(map(lambda tuple: f"question: {tuple[0]}  context:{tuple[1]}", zip(
                    questions, contexts)))
                encoded_inputs = tokenizer(
                    inputs,
                    padding="longest",
                    max_length=max_input_length,
                    truncation=True,
                    return_tensors="pt",
                )
                encoded_targets = tokenizer(
                    answers,
                    padding="longest",
                    max_length=max_input_length,
                    truncation=True,
                    return_tensors="pt",
                )
                encoded_inputs, attention_mask = encoded_inputs.input_ids, encoded_inputs.attention_mask
                encoded_targets = encoded_targets.input_ids

                encoded_inputs = encoded_inputs.to(device)
                encoded_targets = encoded_targets.to(device)
                attention_mask = attention_mask.to(device)
                model_predictions = model.generate(
                    input_ids=encoded_inputs, attention_mask=attention_mask, max_length=max_input_length)

                model_predictions_encoded += model_predictions.tolist()
                target_encoded += encoded_targets.tolist()
        f1, exact_match = validation_set.evaluate(
            target_encoded, model_predictions_encoded)

        print(f"\t Validation F1 = {f1:.2f}, EM = {exact_match:.2f}")
        if f1 > f1_old :
            model.save_pretrained(f'results/{model.name_or_path}/model/best-f1')
            tokenizer.save_pretrained(f'results/{model.name_or_path}/tokenizer/best-f1')
            f1_old = f1
        if epoch+1 % 10 == 0:
            model.save_pretrained(f'results/{model.name_or_path}/model/checkpoint-{epoch+1}')
            tokenizer.save_pretrained(f'results/{model.name_or_path}/tokenizer/checkpoint-{epoch+1}')
        model.train()

    model.save_pretrained(
        f'results/{model.name_or_path}/model/checkpoint-{epoch+1}')
    tokenizer.save_pretrained(
        f'results/{model.name_or_path}/tokenizer/checkpoint-{epoch+1}')

def load_model(model_name: str, device: str) -> T5ForConditionalGeneration:
    """_summary_

    Args:
        model_name (str): _description_
        device (str): _description_

    Returns:
        T5ForConditionalGeneration: _description_
    """
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model.to(device)
    return model

def load_tokenizer(model_name: str) -> PreTrainedTokenizer:
    """_summary_

    Args:
        model_name (str): _description_

    Returns:
        PreTrainedTokenizer: _description_
    """
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    return tokenizer

def predict(model: T5ForConditionalGeneration, tokenizer: PreTrainedTokenizer, question: str, context: str, device: str) -> str:
    """_summary_

    Args:
        model (T5ForConditionalGeneration): _description_
        tokenizer (PreTrainedTokenizer): _description_
        question (str): _description_
        context (str): _description_
        device (str): _description_

    Returns:
        str: _description_
    """
    model.eval()
    inputs = tokenizer.encode(
        f"question: {question}  context: {context}", return_tensors="pt")
    inputs = inputs.to(device)
    outputs = model.generate(inputs, max_length=256, num_return_sequences=5)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI for training T5 T2T model')

    parser.add_argument('--t5_model', type=str, default="google/flan-t5-base",
                        help="What type of T5 model do you want use?")

    parser.add_argument('--batch_size', type=int, default=16,
                        help='mini-batch size (default: 16)')

    parser.add_argument('--epochs', type=int, default=1,
                        help='number of training epochs (default: 40)')

    parser.add_argument('--lr', type=float, default=1e-4,
                        help='learning rate (Adam) (default: 1e-4)')

    parser.add_argument('--workers', type=int, default=10,
                        help='number of working units used to load the data (default: 10)')

    parser.add_argument('--device', default='cuda', type=str,
                        help='device to be used for computations (in {cpu, cuda:0, cuda:1, ...}, default: cpu)')

    parser.add_argument('--max_input_length', type=int, default=512,
                        help='Maximum lenght of input text, (default: 512, maximum admitted: 512)')

    parser.add_argument('--seed', type=int, default=7,
                        help='Seed for random initialization (default: 7)')

    parser.add_argument('--load-check-point-model', type=str, default=None,
                        help='Load a check point to continue training')

    parser.add_argument('--load-check-point-tokenizer', type=str, default=None,
                        help='Load a check point to continue training')                    



    args = parser.parse_args()

    for k, v in args.__dict__.items():
        print(k + '=' + str(v))

    # Set seed
    set_seed(args.seed)

    

    if args.load_check_point_model is not None:
        model = T5ForConditionalGeneration.from_pretrained(args.load_check_point_model)
    else:
        model = T5ForConditionalGeneration.from_pretrained(args.t5_model)
    if args.load_check_point_tokenizer is not None:
        tokenizer = T5Tokenizer.from_pretrained(args.load_check_point_tokenizer)
    else:
        tokenizer = T5Tokenizer.from_pretrained(args.t5_model)
    


    # creating the optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)

    with open('triples.txt') as f:
        lines = [line.replace('(', '').replace(')', '').split(',') for line in f]
    data = pd.DataFrame(lines).iloc[:,:3]
    data[2] = data[2].str.replace('\n', '')
    for j in range(3):
        data[j] = data[j].str.replace('\'', '')
        data[j] = data[j].str.replace('_', ' ')
        data[j] = data[j].str.lower().str.strip()
    data.columns = ['question', 'context', 'answer']

    # randomize the data
    data = data.sample(frac=1).reset_index(drop=True)

    # split the data into train and test

    train_data = data.iloc[:int(len(data)*0.8),:]
    test_data = data.iloc[int(len(data)*0.8):,:]



    train_set = Dataset(train_data, tokenizer, parser=DatasetMap.squad)
    validation_set = Dataset(test_data, tokenizer, parser=DatasetMap.squad)

    train(model=model,
          tokenizer=tokenizer,
          optimizer=optimizer,
          train_set=train_set,
          validation_set=validation_set,
          num_train_epochs=args.epochs, device=args.device, batch_size=args.batch_size)

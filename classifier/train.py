from regex import P
import torch
import os
from model.triple_classifier import TripleClassifier
from model.dataset import TripleDataset
from model.FCloss import FocalLoss
def train(tokenizer_name, model_name, epochs, batch_size, learning_rate):
    # load dataset
    train = TripleDataset("data/triple/training_set.csv", tokenizer_name=tokenizer_name)
    valid =TripleDataset("data/triple/validation_set.csv", tokenizer_name=tokenizer_name)
    test = TripleDataset("data/triple/test_set.csv", tokenizer_name=tokenizer_name)

    

    # load model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TripleClassifier(device, model_name=model_name)
    model.to(device)
    # train model
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    # loss_fn = torch.nn.CrossEntropyLoss()
    loss_fn = FocalLoss(gamma=0.9999, label_smoothing=0.01)
    
    print("Training model...")
    model.train_model(train, valid, epochs, batch_size, optimizer, loss_fn)
    

    # test model
    print("Testing model...")
    print("Test set")
    print("loading model...")
    model.load("model/triple_classifier.pt")
    y_true, y_pred, f1_score, precision, recall, accuracy, confusion_matrix, roc_auc, pr_auc, classification_report = model.test(test, batch_size)

    # threshold tuning
    model.threshold_tuning(y_true, y_pred)



if __name__ == "__main__":
    model_name = "distilbert-base-uncased"
    train(tokenizer_name=model_name, model_name=model_name, epochs=10, batch_size=8, learning_rate=1e-5)
    # test()

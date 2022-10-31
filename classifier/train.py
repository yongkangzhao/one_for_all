from regex import P
import torch
import os
from model.triple_classifier import TripleClassifier
from model.dataset import TripleDataset

def train():
    # load dataset
    train = TripleDataset("data/triple/training_set.csv")
    valid =TripleDataset("data/triple/validation_set.csv")
    test = TripleDataset("data/triple/test_set.csv")

    

    # load model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TripleClassifier(device)
    model.to(device)
    # train model
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    loss_fn = torch.nn.CrossEntropyLoss()
    
    print("Training model...")
    model.train_model(train, valid, 5, 16, optimizer, loss_fn)
    # save model
    model.save("model/triple_classifier.pt")

    # test model
    print("Test set")
    y_true, y_pred, f1_score, precision, recall, accuracy, confusion_matrix, roc_auc, pr_auc, classification_report = model.test(test, 16)

    # threshold tuning
    model.threshold_tuning(y_true, y_pred)



if __name__ == "__main__":

    train()
    # test()

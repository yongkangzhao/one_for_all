import torch
from model.triple_classifier import TripleClassifier
from model.dataset import TripleDataset
from model.FCloss import FocalLoss
import numpy as np
from torch.utils import data
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, roc_auc_score, precision_recall_curve
import argparse
def train(tokenizer_name, model_name, epochs, batch_size, learning_rate):
    # load dataset
    train = TripleDataset("data/triple/training_set.csv", tokenizer_name=tokenizer_name)
    valid =TripleDataset("data/triple/validation_set.csv", tokenizer_name=tokenizer_name)

    

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
    
    model.load("model/triple_classifier.pt")
    return model


def validate(tokenizer_name, model, dataset_path, batch_size):
    test = TripleDataset(dataset_path, tokenizer_name=tokenizer_name)
    # test model
    model.eval()
    y_true = []
    y_pred = []
    y_score = []
    dataset_iter = data.DataLoader(test, batch_size=batch_size, shuffle=False)
    for i, batch in enumerate(dataset_iter):
        output = model(batch["text"].squeeze(1).to(model.device))
        y_true += batch["label"].tolist()
        y_pred += output.argmax(dim=1).tolist()
        y_score += output[:,1].tolist()
    
    threshold = model.threshold_tuning(y_true, y_score)

    # print("F1 score: ", f1_score(y_true, y_pred))
    # print("Precision: ", precision_score(y_true, y_pred))
    # print("Recall: ", recall_score(y_true, y_pred))
    # print("Accuracy: ", accuracy_score(y_true, y_pred))
    # print("ROC AUC: ", roc_auc_score(y_true, y_pred))
    # print("PR AUC: ", precision_recall_curve(y_true, y_pred))

    y_pred = [1 if i > threshold else 0 for i in y_score]
    # print("Threshold: ", threshold)
    print("Classification report: \n", classification_report(y_true, y_pred))
    print("Confusion matrix: \n", confusion_matrix(y_true, y_pred))
    return y_true, y_score
    

def threshold_tuning(y_true, y_pred, metrics, precision_target, **kwargs):
    # metrics: f1, precision, recall, accuracy, roc_auc, pr_auc
    # kwargs: upper bound, lower bound
    # return: threshold

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    best_score = 0
    best_threshold = 0
    for threshold in sorted(y_pred, reverse=False):
        y_hat = (y_pred >= threshold) * 1
        score = metrics(y_true, y_hat, **kwargs)
        # print("positive: ","threshold: ", threshold, "score: ", score)
        if score > best_score:
            best_score = score
            best_threshold = threshold
            if best_score >= precision_target:
                break
    if best_score < precision_target:
        print("Warning: best score is lower than precision target")
        best_threshold = 1
    upper = best_threshold


    y_true = (y_true == 0) * 1
    y_pred =  1 - y_pred

    best_score = 0
    best_threshold = 0
    for threshold in sorted(y_pred, reverse=False):
        y_hat = (y_pred >= threshold) * 1
        score = metrics(y_true, y_hat, **kwargs)
        # print("negative: ","threshold: ", threshold, "score: ", score)
        if score > best_score:
            best_score = score
            best_threshold = threshold
            if best_score >= precision_target:
                break
    
    if best_score < precision_target:
        print("Warning: best score is lower than precision target")
        best_threshold = 0
    lower = best_threshold

    return upper, 1-lower

def classsification_report_with_threshold(y_true, y_pred, upper, lower):
    y_true = np.array(y_true)
    y_hat = np.array(y_pred)
    y_hat[y_hat >= upper] = 1
    y_hat[y_hat <= lower] = 0
    y_hat[(y_hat > 0) & (y_hat < 1)] = 2
    print(classification_report(y_true[y_hat<2], y_hat[y_hat<2]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="bert-base-uncased")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=1e-5)
    parser.add_argument("--precision_target", type=float, default=0.95)
    parser.add_argument("--train", type=int, default=1)
    
    args = parser.parse_args()


    model_name = args.model_name
    epochs = args.epochs
    batch_size = args.batch_size
    learning_rate = args.learning_rate
    precision_target = args.precision_target
    if args.train:
        print("Building model...")
        model = train(tokenizer_name=model_name, model_name=model_name, epochs=args.epochs, batch_size=args.batch_size, learning_rate=args.learning_rate)
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = TripleClassifier(device, model_name=model_name)
        model.load("model/"+model_name+"_triple_classifier.pt")
    print("Validating model...")
    y_true, y_pred = validate(tokenizer_name=model_name, model=model, dataset_path = 'data/triple/validation_set.csv', batch_size=args.batch_size)
    print("Tuning threshold...")
    upper, lower = threshold_tuning(y_true, y_pred, precision_score, precision_target=args.precision_target, pos_label=1)
    print("upper: ", upper, "lower: ", lower)
    print("Classification report with threshold applied on validation set: ")
    classsification_report_with_threshold(y_true, y_pred, upper, lower)
    print("Testing model...")
    y_true, y_pred = validate(tokenizer_name=model_name, model=model, dataset_path = 'data/triple/test_set.csv', batch_size=args.batch_size)
    print("Classification report with threshold applied on test set: ")
    classsification_report_with_threshold(y_true, y_pred, upper, lower)
    if args.train:
        print("saving model...")
        model.save("model/"+model_name+"_triple_classifier.pt")
    print("saving threshold...")
    with open("model/"+model_name+"_threshold_triple_classifier.txt", "w") as f:
        f.write(str(upper) + "\n")
        f.write(str(lower) + "\n")
    


    # test()

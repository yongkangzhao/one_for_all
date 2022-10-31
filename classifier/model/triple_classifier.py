from transformers import AutoModel
import torch
from torch.utils import data
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, roc_auc_score, precision_recall_curve
scaler = torch.cuda.amp.GradScaler()

class TripleClassifier(torch.nn.Module):
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.model = AutoModel.from_pretrained("distilbert-base-uncased")
        self.fc1 = torch.nn.Linear(768, 768)
        self.fc2 = torch.nn.Linear(768, 2)
        self.softmax = torch.nn.Softmax(dim=1)
        self.relu = torch.nn.ReLU()
        
    def forward(self, tokens):
        output = self.model(tokens)[0][:,0,:]
        
        output = self.relu(self.fc1(output))
        output = self.fc2(output)
        output = self.softmax(output)

        return output

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))
    
    def train_model(self, training_dataset, validation_dataset, epochs, batch_size, optimizer, loss_fn):
        self.train()
        best_f1 = 0

        training_dataset_iter = data.DataLoader(training_dataset, batch_size=batch_size, shuffle=True)

        for epoch in range(epochs):
            # for i in range(0, len(training_dataset), batch_size):
            #     optimizer.zero_grad()
            #     with torch.cuda.amp.autocast(dtype=torch.float):
            #         batch = training_dataset[i:i+batch_size]
                    
            #         loss = 0
            #         for j in range(len(batch)):
            #             output = self(batch.iloc[j]["text"])
            #             loss += loss_fn(output, torch.tensor([batch.iloc[j]["label"]]).to(self.device))
            #     scaler.scale(loss).backward()
            #     scaler.step(optimizer)
            #     scaler.update()
            #     if i % 100 == 0:
            #         print("Epoch: ", epoch, " Batch: ", i, " Loss: ", loss.item())
            for i, batch in enumerate(training_dataset_iter):
                optimizer.zero_grad()
                with torch.cuda.amp.autocast(dtype=torch.float):
                    output = self(batch["text"].squeeze(1).to(self.device))
                    loss = loss_fn(output, batch["label"].to(self.device))
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
                if i % 10 == 0:
                    print("Epoch: ", epoch, " Batch: ", i, " Loss: ", loss.item())
                
            

            print("Validation set: ")
            y_true, y_pred, f1_score, precision, recall, accuracy, confusion_matrix, roc_auc, pr_auc, classification_report = self.test(validation_dataset, batch_size)
            print("F1 score: ", f1_score)
            if f1_score > best_f1:
                best_f1 = f1_score
                self.save("model/triple_classifier.pt")
                print("Model saved")

    def test(self, dataset, batch_size):
        # f1 score
        # precision
        # recall
        # accuracy
        # roc curve
        # pr curve
        # classification report
        # confusion matrix
        self.eval()
        y_true = []
        y_pred = []
        y_score = []
        dataset_iter = data.DataLoader(dataset, batch_size=batch_size, shuffle=False)
        for i, batch in enumerate(dataset_iter):
            output = self(batch["text"].squeeze(1).to(self.device))
            y_true += batch["label"].tolist()
            y_pred += output.argmax(dim=1).tolist()
            y_score += output[:,1].tolist()
        
        

        # print("F1 score: ", f1_score(y_true, y_pred))
        # print("Precision: ", precision_score(y_true, y_pred))
        # print("Recall: ", recall_score(y_true, y_pred))
        # print("Accuracy: ", accuracy_score(y_true, y_pred))
        # print("ROC AUC: ", roc_auc_score(y_true, y_pred))
        # print("PR AUC: ", precision_recall_curve(y_true, y_pred))
        print("Classification report: \n", classification_report(y_true, y_pred))
        print("Confusion matrix: \n", confusion_matrix(y_true, y_pred))
        return y_true, y_score, f1_score(y_true, y_pred), precision_score(y_true, y_pred), recall_score(y_true, y_pred), accuracy_score(y_true, y_pred), confusion_matrix(y_true, y_pred), roc_auc_score(y_true, y_pred), precision_recall_curve(y_true, y_pred), classification_report(y_true, y_pred)

    def threshold_tuning(self, y_true, y_pred):
        
        for i in sorted(set(y_pred)):
            y_pred_new = [1 if x >= i else 0 for x in y_pred]
            # print("Threshold: ", i, " F1 score: ", f1_score(y_true, y_pred_new), " Precision: ", precision_score(y_true, y_pred_new), " Recall: ", recall_score(y_true, y_pred_new))
            # print("Classification report: \n", classification_report(y_true, y_pred_new))
            # print("Confusion matrix: \n", confusion_matrix(y_true, y_pred_new))

        # find the best threshold for positive class with higher than 0.9 precision
        best_positive_threshold = 0
        for i in sorted(set(y_pred)):
            y_pred_new = [1 if x >= i else 0 for x in y_pred]
            if precision_score(y_true, y_pred_new) >= 0.9:
                print("Best threshold: ", i)
                best_positive_threshold = i
                break
        
        # find the best threshold for negative class with higher than 0.9 precision
        best_negative_threshold = 0
        for i in sorted(set(y_pred), reverse=True):
            y_pred_new = [1 if x >= i else 0 for x in y_pred]
            if precision_score(y_true, y_pred_new) >= 0.9:
                print("Best threshold: ", i)
                best_negative_threshold = i
                break
        
        # use both thresholds as upper and lower bound, ignore the middle part and show the classification report
        positives = np.array(y_pred) >= best_positive_threshold
        negatives = np.array(y_pred) <= best_negative_threshold
        null = np.logical_or(np.array(y_pred) <= best_positive_threshold, np.array(y_pred) >= best_negative_threshold)
        y_pred_new = np.array(y_pred.copy())
        y_pred_new[positives] = 1
        y_pred_new[negatives] = 0
        y_pred_new[~null] = 2

        y_true_new = np.array(y_true.copy())
        y_true_new[~null] = 2
        

        print("Classification report: \n", classification_report(y_true_new, y_pred_new))


    
    def predict(self, text, threshold=0.5):
        self.eval()
        output = self(text)
        if output[0][0] >= threshold:
            return 0
        else:
            return 1
        

    

if __name__ == "__main__":
    tripleClassifier = TripleClassifier()
    prediction = tripleClassifier('money [SEP] entity_type: motivation [SEP] being [persona] is caused by the need of [MASK] and: "{ "count": 2, "being supporter is caused by the need of [MASK] and": { "money": { "count": 2 } } }"')
    print(prediction)


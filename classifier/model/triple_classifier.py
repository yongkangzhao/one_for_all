from transformers import AutoModel
import torch
from torch.utils import data
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, roc_auc_score, precision_recall_curve
from sklearn.model_selection import StratifiedKFold


scaler = torch.cuda.amp.GradScaler()

class TripleClassifier(torch.nn.Module):
    def __init__(self, device, model_name='distilbert-base-uncased-finetuned-sst-2-english'):
        super().__init__()
        self.device = device
        self.model = AutoModel.from_pretrained(model_name)
        self.fc1 = torch.nn.Linear(768, 768//2)
        self.fc2 = torch.nn.Linear(768//2, 768//4)
        self.fc3 = torch.nn.Linear(768//4, 2)
        self.softmax = torch.nn.Softmax(dim=1)
        self.sigmoid = torch.nn.Sigmoid()
        self.relu = torch.nn.ReLU()
        
    def forward(self, tokens):
        output = self.model(tokens)[0][:,0,:]
        
        output = self.relu(self.fc1(output))
        output = self.relu(self.fc2(output))
        output = self.fc3(output)
        output = self.softmax(output)

        return output

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))
    
    def train_model(self, training_dataset, validation_dataset, epochs, batch_size, optimizer, loss_fn):
        
        best_f1 = 0

        training_dataset_iter = data.DataLoader(training_dataset, batch_size=batch_size, num_workers=4, sampler=StratifiedBatchSampler(torch.tensor(training_dataset.dataset['label']), batch_size=batch_size))

        count = 0
        for epoch in range(epochs):
            self.train()
            for i, batch in enumerate(training_dataset_iter):
                optimizer.zero_grad()
                output = self(batch["text"].squeeze(1).to(self.device))
                with torch.cuda.amp.autocast(dtype=torch.float):
                    loss = loss_fn(output[:, 1], batch["label"].type(torch.float).to(self.device))
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
                if i % 10 == 0:
                    print("Epoch: ", epoch, " Batch: ", i, " Loss: ", loss.item())
            print("Validation set: ")
            f1_score = self.test(validation_dataset, batch_size)
            print("F1 score: ", f1_score)
            if f1_score > best_f1:
                best_f1 = f1_score
                self.save("model/triple_classifier.pt")
                print("Model saved")
                count = 0
            else:
                count += 1
                if count == 5:
                    # lower learning rate
                    for param_group in optimizer.param_groups:
                        param_group['lr'] = param_group['lr'] / 2
                    count = 0
                    print("Learning rate lowered")
                if count == 10:
                    print("Early stopping after 10 epochs without improvement")
                    break

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
        
        threshold = self.threshold_tuning(y_true, y_score)

        # print("F1 score: ", f1_score(y_true, y_pred))
        # print("Precision: ", precision_score(y_true, y_pred))
        # print("Recall: ", recall_score(y_true, y_pred))
        # print("Accuracy: ", accuracy_score(y_true, y_pred))
        # print("ROC AUC: ", roc_auc_score(y_true, y_pred))
        # print("PR AUC: ", precision_recall_curve(y_true, y_pred))

        y_pred = [1 if i > threshold else 0 for i in y_score]
        print("Threshold: ", threshold)
        print("Classification report: \n", classification_report(y_true, y_pred))
        print("Confusion matrix: \n", confusion_matrix(y_true, y_pred))
        return f1_score(y_true, y_pred)

    def threshold_tuning(self, y_true, y_pred):
        # maximize f1 score
        best_threshold = 0
        best_f1 = 0
        for i in sorted(set(y_pred)):
            y_pred_new = [1 if j > i else 0 for j in y_pred]
            f1 = f1_score(y_true, y_pred_new, average='macro')
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = i
        return best_threshold

    
    def predict(self, text, upper, lower):
        self.eval()
        y_pred = self(text)
        y_hat = np.array(y_pred)
        y_hat[y_hat >= upper] = 1
        y_hat[y_hat <= lower] = 0
        y_hat[(y_hat > 0) & (y_hat < 1)] = 2
        return y_hat

class StratifiedBatchSampler:
    """Stratified batch sampling
    Provides equal representation of target classes in each batch
    """
    def __init__(self, y, batch_size, shuffle=True):
        if torch.is_tensor(y):
            y = y.numpy()
        assert len(y.shape) == 1, 'label array must be 1D'
        n_batches = int(len(y) / batch_size)
        self.skf = StratifiedKFold(n_splits=n_batches, shuffle=shuffle)
        self.X = torch.randn(len(y),1).numpy()
        self.y = y
        self.shuffle = shuffle

    def __iter__(self):
        if self.shuffle:
            self.skf.random_state = torch.randint(0,int(1e8),size=()).item()
        idx = []
        for train_idx, test_idx in self.skf.split(self.X, self.y):
            idx.extend(test_idx)
        return iter(idx)

    def __len__(self):
        return len(self.y)

        

    

if __name__ == "__main__":
    tripleClassifier = TripleClassifier()
    prediction = tripleClassifier('money [SEP] entity_type: motivation [SEP] being [persona] is caused by the need of [MASK] and: "{ "count": 2, "being supporter is caused by the need of [MASK] and": { "money": { "count": 2 } } }"')
    print(prediction)


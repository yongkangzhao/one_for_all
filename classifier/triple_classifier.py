from transformers import AutoTokenizer, AutoModel
import torch

class Triple_classifier(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")

        self.fc1 = torch.nn.Linear(768, 768)
        self.fc2 = torch.nn.Linear(768, 2)
        self.softmax = torch.nn.Softmax(dim=1)
        self.relu = torch.nn.ReLU()
        
    def forward(self, text):
        token = self.tokenizer.encode(text, add_special_tokens=True)
        token = torch.tensor(token).unsqueeze(0)
        output = self.model(token)[0][:,0,:]
        output = self.fc1(output)
        output = self.relu(self.fc2(output))
        output = self.softmax(output)

        return output


if __name__ == "__main__":
    triple_classifier = Triple_classifier()
    prediction = triple_classifier('money [SEP] entity_type: motivation [SEP] being [persona] is caused by the need of [MASK] and: "{ "count": 2, "being supporter is caused by the need of [MASK] and": { "money": { "count": 2 } } }"')
    print(prediction)


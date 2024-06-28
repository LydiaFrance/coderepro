import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModel, AutoTokenizer

# TODO: find a better way to host the model
# if you run this for the first time, make sure you get the model first
# mkdir data
# wget https://cernbox.cern.ch/remote.php/dav/public-files/QV47M3dk0eXGdbe/bert_classifier.pt

#some defines that are needed for the model
class Classifier(nn.Module):
    def __init__(self, embedding_model, n_classes, dropout_p=0.1, train_embedder=True):
        super().__init__()
        self.embedding_model = AutoModel.from_pretrained(embedding_model)
        self.dropout = nn.Dropout(dropout_p)
        self.linear = nn.Linear(self.embedding_model.config.hidden_size, n_classes)

        if not train_embedder:
            for param in self.embedding_model.parameters():
                param.requires_grad = False

    def forward(self, input_ids, attention_mask):
        outputs = self.embedding_model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        pooled_output = last_hidden_state[:, 0]
        pooled_output = self.dropout(pooled_output)
        logits = self.linear(pooled_output)
        return logits

class TextClassificationDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        inputs = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_tensors='pt',
            truncation=True
        )
        return {
            'input_ids': inputs['input_ids'].flatten(),
            'attention_mask': inputs['attention_mask'].flatten(),
            'label': torch.tensor(label)
        }
 

def evaluate_bert(text):
    path_to_model = "./data/bert_classifier.pt"
    # evaluate on cpu for now
    device = 'cpu'

    # load the mode, now on CPU
    model = torch.load(path_to_model, map_location=torch.device(device))
    model.eval()

    #now create sth from the text that BERT understands (TODO: the label is an artifact from the training code and should be removed)
    tokenizer = AutoTokenizer.from_pretrained('distilbert/distilbert-base-uncased')
    max_len = 128
    batch_size = 16

    eval_data = TextClassificationDataset([text], [1], tokenizer, max_len)
    eval_loader = DataLoader(eval_data, batch_size=batch_size, shuffle=False)
    batch = next(iter(eval_loader))

    with torch.no_grad():
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)

        outputs = model(input_ids, attention_mask)
        probs = nn.functional.softmax(outputs, dim=1)
        return probs[0, 1].item()*100
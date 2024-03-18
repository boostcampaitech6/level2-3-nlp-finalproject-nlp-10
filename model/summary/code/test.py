from transformers import AutoTokenizer, BartForConditionalGeneration, AutoConfig, Trainer, TrainingArguments, AutoFeatureExtractor, set_seed, AdamW
import torch
import pandas as pd
import numpy as np
import os
import random
from argparse import ArgumentParser
from tqdm import tqdm, trange
import json
from data_load import load_dataset
from torch.utils.data import Dataset, DataLoader, TensorDataset, RandomSampler
from make_dataset import make_dataset
import torch.nn as nn
import torch.optim as optim
from rouge import Rouge

seed = 1997

random.seed(seed) # python random seed 고정
np.random.seed(seed) # numpy random seed 고정
torch.manual_seed(seed) # torch random seed 고정
torch.cuda.manual_seed_all(seed)
set_seed(seed)

test_dataset_path = '../dataset'
test_data = pd.read_csv(os.path.join(test_dataset_path, "samsung_feb.csv"))

length_penalty=2.0,
max_length=203,
min_length=30,
num_beams=6,
repetition_penalty=2.0,
no_repeat_ngram_size = 15

print(test_data.head(2))
context = test_data['contents']
print(context.head(3))

model_name = "ainize/kobart-news"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = torch.load('../trained_model/model.pt')
model2 = BartForConditionalGeneration.from_pretrained(model_name).to("cuda")
torch.cuda.empty_cache()

with torch.no_grad():
    model.eval()
    model2.eval()

    for i in range(800,840):
        #if len(context[i])>1024:continue
        input_ids = tokenizer.encode(context[i], return_tensors="pt", padding="max_length", truncation=True, max_length=1026)

        summary_text_ids = model.generate(
        input_ids=input_ids.to("cuda"),
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        length_penalty=length_penalty,
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        )

        summary_text_ids2 = model2.generate(
        input_ids=input_ids.to("cuda"),
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        length_penalty=length_penalty,
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        )

        print(i, ': ', context[i])
        print(len(tokenizer.tokenize(context[i])))
        print()
        print(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True))
        print(len(summary_text_ids[0]))
        print()
        print(tokenizer.decode(summary_text_ids2[0], skip_special_tokens=True))
        print(len(summary_text_ids2[0]))
        print('\n\n')

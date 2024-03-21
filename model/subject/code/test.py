from transformers import AutoTokenizer, BartForConditionalGeneration, TrainingArguments, set_seed
import torch
import pandas as pd
import numpy as np
import os
from tqdm import tqdm, trange
import random
from data_load import load_dataset, read_csv
from make_dataset import make_dataset
from torch.utils.data import DataLoader, RandomSampler
from prepocess import remove_between_square_brackets, remove_space

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


model_path = "../trained_model"
data_path = "../dataset"
model_name = "EbanLee/kobart-title"
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

df = load_dataset(os.path.join(data_path, "Validation/edit_valid_dataset.json"), tokenizer)     #[title, context]
target = df['title'].to_list()

while(True):
    idx = input(f"Index 입력(최대 {len(target)-1}), 직접입력:'str' :")
    if idx == 'str':
        text = input(f"Input Text :")

        input_ids = tokenizer.encode(text, return_tensors="pt", padding="max_length", truncation=True, max_length=1026)

        summary_text_ids = model.generate(
                                input_ids=input_ids.to(device),
                                bos_token_id=model.config.bos_token_id,
                                eos_token_id=model.config.eos_token_id,
                                length_penalty=1.0,
                                max_length=40,
                                min_length=3,
                                num_beams=6,
                                repetition_penalty=1.5,
                                ).to("cpu")

        print(f"원문 : {text}\n")
        print(f"예측 : {remove_space(remove_between_square_brackets(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)))}\ttoken_n={len(summary_text_ids[0])-2}")

    else:
        idx = int(idx)

        input_ids = tokenizer.encode(df['context'].iloc[idx], return_tensors="pt", padding="max_length", truncation=True, max_length=1026)

        summary_text_ids = model.generate(
                                input_ids=input_ids.to(device),
                                bos_token_id=model.config.bos_token_id,
                                eos_token_id=model.config.eos_token_id,
                                length_penalty=1.0,
                                max_length=40,
                                min_length=3,
                                num_beams=6,
                                repetition_penalty=1.5,
                                ).to("cpu")

        print(f"원문 : {df['context'].iloc[idx]}\n")
        print(f"예측 : {remove_space(remove_between_square_brackets(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)))}\t(token_n={len(summary_text_ids[0])-2})")
        print(f"제목 : {target[idx]}\n")

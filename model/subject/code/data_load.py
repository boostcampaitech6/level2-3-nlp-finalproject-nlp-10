import torch
import pandas as pd
import numpy as np
import os
from tqdm import tqdm, trange
import json
from prepocess import pre_processing

def load_dataset(path, tokenizer):
    df = pd.read_json(path)['documents']
    total = {'title' : [], 'context' : []}

    for d in tqdm(df, desc=f"make_df .json "):
        total_s=''
        for texts in d['text']:
            for text in texts:
                total_s+=text['sentence']
        if len(tokenizer.tokenize(total_s))<50: 
            continue

        title = pre_processing(d['title'])
        total['title'].append(title)
        total['title'].append(title)
        total['context'].append(d['abstractive'][0])
        total['context'].append(total_s)

    total_df = pd.DataFrame(total)

    return total_df

def read_csv(path, tokenizer):
    df = pd.read_csv(path)
    total = {'title' : [], 'context' : []}

    for idx in trange(len(df), desc=f"make_df .csv"):
        if len(tokenizer.tokenize(df['contents'].iloc[idx]))<50:
            continue

        title = pre_processing(df['title'].iloc[idx])
        total['title'].append(title)
        total['context'].append(df['contents'].iloc[idx])
        total['title'].append(title)
        total['context'].append(df['summary'].iloc[idx])
        
    total_df = pd.DataFrame(total)

    return total_df
